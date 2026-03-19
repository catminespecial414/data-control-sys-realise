def execute_analysis_and_save():
    """读取传感器 -> 尝试识别图片 -> 强制写入数据库"""
    
    # 1. 采集环境数据 (先执行，保证数据实时性)
    time.sleep(1.0) # 给系统喘息时间
    sensor_data = sensor_manager.get_all_data()
    t = sensor_data.get('temperature', 0)
    h = sensor_data.get('humidity', 0)
    s = sensor_data.get('soil', 0)      
    l = sensor_data.get('light', 0)
    p = sensor_data.get('ph', 7.0)

    # 2. 尝试从共享字典获取画面进行 AI 识别
    aphid, armyworm, beetle = 0, 0, 0
    current_img = None
    
    with lock:
        if state['frame'] is not None:
            current_img = state['frame'].copy()
    
    # 如果画面就绪，执行 AI 逻辑
    if current_img is not None:
        try:
            print("📸 [AI] 正在识别画面...")
            res = ai_engine.analyze(current_img)
            aphid = res.count("蚜虫")
            armyworm = res.count("粘虫")
            beetle = res.count("瓢虫") + res.count("天牛") + res.count("甲虫")
            print(f"✅ [Auto AI] 识别成功：蚜虫:{aphid}, 粘虫:{armyworm}, 甲虫:{beetle}")
        except Exception as e:
            print(f"❌ [AI Error] 识别出错: {e}")
    else:
        # 画面为空时不再 return，而是记录一条日志并继续往下走
        print("ℹ️ [AI] 画面暂未就绪，本次跳过害虫计数")

    # 3. 核心步骤：将数据存入数据库 (无论是否有画面，都会执行)
    try:
        insert_env_data(t, h, s, l, p, aphid, armyworm, beetle)
        print(f"💾 [Database] 数据已保存：T:{t} H:{h} Pests:{aphid+armyworm+beetle}")
    except Exception as e:
        print(f"❌ [Database Error] 存入失败: {e}")