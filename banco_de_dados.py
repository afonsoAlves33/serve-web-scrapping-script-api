import pyodbc
import datetime


class banco_de_dados():
    def __init__(self):
        conn_str = (
            "Driver={ODBC Driver 18 for SQL Server};"
            "Server=hololenstcc.database.windows.net;"
            "Database=free-sql-db;"
            "UID=sqlroot;"
            "PWD=Google.com;"
        )
        self.conn = pyodbc.connect(conn_str, timeout=90)
        self.cursor = self.conn.cursor()
        self.criar_tabela_caso_nao_exista()

    async def criar_tabela_caso_nao_exista(self) -> int:
        sql = """
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Ocorrencias' AND xtype='U')
                BEGIN
                    CREATE TABLE Ocorrencias (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        data DATE,
                        hora NVARCHAR(15),
                        tipo NVARCHAR(50),
                        ordem NVARCHAR(50),
                        descricao NVARCHAR(255),
                        equipamento NVARCHAR(100)
                    );
                END
                """
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
            return -1
        self.conn.commit()
        return 1

    def executar_query(self, query) -> any:
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(e)
            return -1
        self.res = self.cursor.fetchall()
        for linha in self.res:
            print(linha)
        return self.res

    def formatar_data(self, dados):
        data_formatada = dados
        return data_formatada[-4] + data_formatada[-3] + data_formatada[-2] + data_formatada[-1] + "-" + data_formatada[
            -7] + data_formatada[-6] + "-" + data_formatada[-10] + data_formatada[-9]

    def inserir_dados(self, dados) -> int:
        data_formatada = self.formatar_data(dados.data)
        hora = dados.hora
        tipo = dados.tipo
        ordem = dados.ordem
        descricao = dados.descricao
        equipamento = dados.equipamento

        query = f"""
            INSERT INTO Ocorrencias (hora, data, tipo, ordem, descricao, equipamento)
            VALUES ('{hora}', '{data_formatada}',  '{tipo}', '{ordem}', '{descricao}', '{equipamento}');
        """
        print(query)
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(e)
            return -1
        self.conn.commit()
        return 1

    def conferir_data_e_hora(self, hora, data, hora2, data2):
        data_e_tempo = datetime.datetime(year=int(data[6:]), month=int(data[3:5]), day=int(data[:2]),
                                         hour=int(hora[:2]), minute=int(hora[3:5]))
        data_e_tempo_2 = datetime.datetime(year=int(data2[6:]), month=int(data2[3:5]), day=int(data2[:2]),
                                           hour=int(hora2[:2]), minute=int(hora2[3:5]))
        return data_e_tempo >= data_e_tempo_2

    def obter_ultimo_registro(self):
        try:
            sql = """
                SELECT TOP 1 
                CONVERT(VARCHAR(10), data, 103) AS data_formatada, -- Formato brasileiro 'dd/MM/yyyy'
                hora
                FROM Ocorrencias
                ORDER BY data DESC, hora DESC;
            """
            self.cursor.execute(sql)
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado
            return None
        except Exception as e:
            print(f"Erro ao obter o último registro: {e}")
            return None
        
    def obter_registros(self):
        try:
            sql = """
                SELECT * FROM Ocorrencias ORDER BY data DESC, hora DESC;
            """
            self.cursor.execute(sql)
            resultado = self.cursor.fetchall()
            if resultado:
                return resultado
            return None
        except Exception as e:
            raise 


if __name__ == '__main__':  # mudar ordem caso de ruim
    bd = banco_de_dados()
    print(bd.executar_query("SELECT * FROM Ocorrencias;"))
    # print(bd.inserir_dados({'hora': '09:33:00', 'data': '16/09/2024', 'tipo': 'ZM11', 'ordem': '908501121273', 'descricao': 'falha no cilindro da garra que puxa o bl', 'equipamento': '877000004440-510 Modulo 5 - Estação 5510 - Paletizador BH'}))
    # bd.conferir_data_e_hora('09:33:00', '16/09/2024', '09:33:00', '16/09/2024')