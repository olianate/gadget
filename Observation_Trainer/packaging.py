# 导入需要打包的主模块
import main

# 打包配置
opts = {
    'name': 'Observation Trainer',
    'noconsole': True  # 可选，不显示控制台窗口
}

# 使用PyInstaller打包
if __name__ == '__main__':
    import PyInstaller.__main__

    args = [
        '--onefile',
        '--windowed',
        f"--name={opts['name']}",
        f"--icon={opts['icon']}" if 'icon' in opts else '',
        "--noconsole" if opts.get('noconsole', False) else '',
        main.__file__,
    ]

    PyInstaller.__main__.run(args)
