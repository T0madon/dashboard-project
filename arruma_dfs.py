import os
import pandas as pd

PASTA = "dataframes"

NOME_ERRADO = "Departamento de Biologia Estrutural, Molecular e GenÃ©tica"
NOME_CORRETO = "Departamento de Biologia Estrutural, Molecular e Genética"

def carregar_csv_corrigido(caminho):
    """
    Lê um CSV garantindo que linhas quebradas (com vírgula no meio do nome do departamento)
    sejam reagrupadas corretamente.
    """
    linhas_corrigidas = []
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        buffer = ""
        for linha in f:
            linha = linha.strip("\n")
            # Junta pedaços de linhas quebradas
            if buffer:
                buffer += " " + linha
                if buffer.count(",") >= 1:  # condição mínima para linha válida
                    linhas_corrigidas.append(buffer)
                    buffer = ""
            else:
                if linha.count(",") < 1:  # linha quebrada (não tem separador suficiente)
                    buffer = linha
                else:
                    linhas_corrigidas.append(linha)
        # Se sobrar algo no buffer, adiciona
        if buffer:
            linhas_corrigidas.append(buffer)

    # Cria DataFrame
    from io import StringIO
    csv_corrigido = "\n".join(linhas_corrigidas)
    return pd.read_csv(StringIO(csv_corrigido), sep=",", engine="python")

def limpar_dataframes(pasta):
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".csv"):
            caminho = os.path.join(pasta, arquivo)
            print(f"Processando: {caminho}")

            try:
                df = carregar_csv_corrigido(caminho)

                if "departamento" in df.columns:
                    # Corrige o nome errado
                    df["departamento"] = df["departamento"].replace(NOME_ERRADO, NOME_CORRETO)

                    # Remove linhas com departamento vazio ou NaN
                    df = df[df["departamento"].notna()]
                    df = df[df["departamento"].str.strip() != ""]

                # Salva sobrescrevendo
                df.to_csv(caminho, index=False, encoding="utf-8-sig")

            except Exception as e:
                print(f"Erro ao processar {arquivo}: {e}")

if __name__ == "__main__":
    limpar_dataframes(PASTA)
    print("✅ Todos os dataframes foram processados e corrigidos!")