import csv
import sys

# 设置标准输出编码为utf-8，防止中文乱码
sys.stdout.reconfigure(encoding='utf-8')

def process_pokemon_csv(input_file):
    shiny_pokemon = set()
    non_shiny_pokemon = set()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader) # 跳过表头
            
            # 找到Nickname和IsShiny的列索引
            try:
                nickname_idx = headers.index("Nickname")
                species_idx = headers.index("Species") # 备用，如果Nickname太复杂
                is_shiny_idx = headers.index("IsShiny")
                position_idx = headers.index("Position") # 用来辅助判断闪光
            except ValueError:
                print("Error: Required columns not found")
                return

            for row in reader:
                if not row: continue
                
                # 获取宝可梦名字（优先用Species，因为它比较干净，Nickname有时包含特殊字符）
                name = row[species_idx]
                
                # 判断是否闪光
                # 逻辑1: 直接看 IsShiny 列
                is_shiny = row[is_shiny_idx].lower() == 'true'
                
                # 逻辑2: 辅助判断，看Position列里是否有 ★ (这是用户提到的)
                # 比如: "main @ [01] (Box 1)-01: 0001 ★ - 妙蛙种子..."
                position_str = row[position_idx]
                if '★' in position_str:
                    is_shiny = True
                
                if is_shiny:
                    shiny_pokemon.add(name)
                else:
                    non_shiny_pokemon.add(name)
                    
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # 排序输出到文件
    output_txt = r"d:\chromedownload\批量产图\pokemon_list.txt"
    try:
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write("【闪光宝可梦 (Shiny)】\n")
            for name in sorted(list(shiny_pokemon)):
                f.write(f"★ {name}\n")
            
            f.write("\n【普通宝可梦 (Non-Shiny)】\n")
            for name in sorted(list(non_shiny_pokemon)):
                f.write(f"{name}\n")
        print(f"列表已保存到: {output_txt}")
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    input_csv = r"d:\chromedownload\批量产图\全部宝可梦数据excel含dlc.csv"
    process_pokemon_csv(input_csv)
