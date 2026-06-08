import json
import csv

def reduce_jsonl_to_csv(jsonl_path, csv_path, keys_to_extract, limit=50000):
    """
    Função utilitária para extrair apenas as chaves necessárias de um arquivo JSONL gigante,
    convertendo-o para um arquivo CSV menor e otimizado para o consumo do Pandas.
    """
    with open(jsonl_path, 'r', encoding='utf-8') as f_in, \
         open(csv_path, 'w', encoding='utf-8', newline='') as f_out:
        
        writer = csv.DictWriter(f_out, fieldnames=keys_to_extract)
        writer.writeheader()
        
        count = 0
        for line in f_in:
            if count >= limit:
                break
            try:
                data = json.loads(line)
                # Extrai apenas as colunas vitais para o projeto
                row = {k: data.get(k, '') for k in keys_to_extract}
                writer.writerow(row)
                count += 1
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    print("Iniciando redução dos metadados do Catálogo...")
    reduce_jsonl_to_csv(
        jsonl_path="data/meta_Automotive.jsonl",
        csv_path="data/amazon_meta_automotive_sample.csv",
        keys_to_extract=["parent_asin", "title", "price", "average_rating"],
        limit=50000
    )
    
    print("Iniciando redução dos Reviews de Usuários...")
    reduce_jsonl_to_csv(
        jsonl_path="data/Automotive.jsonl",
        csv_path="data/amazon_reviews_automotive_sample.csv",
        keys_to_extract=["user_id", "parent_asin", "rating", "timestamp"],
        limit=50000
    )
    
    print("Processo finalizado! Arquivos CSV limpos e gerados na pasta data/.")
