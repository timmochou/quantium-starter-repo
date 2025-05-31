#!/bin/bash

# 設置錯誤時退出
set -e

echo "開始運行測試套件..."

# 檢查是否在虛擬環境中
if [ -z "$VIRTUAL_ENV" ]; then
    echo "正在啟動虛擬環境..."
    # 如果使用 conda
    if command -v conda &> /dev/null; then
        # 初始化 conda
        eval "$(conda shell.bash hook)"
        conda activate Quantium
    # 如果使用 venv
    elif [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "錯誤：找不到虛擬環境"
        exit 1
    fi
fi

# 安裝依賴
echo "安裝依賴..."
pip install -r requirements.txt

# 確保在正確的目錄中
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 運行測試
echo "運行測試..."
pytest test_task5.py -v

# 保存測試結果
TEST_RESULT=$?

# 如果測試失敗，返回錯誤碼 1
if [ $TEST_RESULT -ne 0 ]; then
    echo "測試失敗！"
    exit 1
fi

echo "所有測試通過！"
exit 0