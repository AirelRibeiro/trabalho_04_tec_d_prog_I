import matplotlib.pyplot as plt


class PlotManager:

    @staticmethod
    def plot_route(df):
        plt.figure(figsize=(16, 8))

        # Cores com base na quantidade de material
        colors = df["quantidade_material"].head(75).tolist()

        # Plot dos pontos com coloração baseada na quantidade de material
        sc = plt.scatter(df["longitude"].head(75).tolist(
        ), df["latitude"].head(75).tolist(), c=colors, cmap='Reds')

        # Conectando os pontos com linhas
        plt.plot(df["longitude"].head(75).tolist(), df["latitude"].head(
            75).tolist(), c='blue', linestyle='-', label='Rota')

        # Adicionando quantidade de material em cada ponto
        offset = 0.005
        for index, row in df.head(75).iterrows():
            if 200 <= row['quantidade_material'] <= 262:
                plt.text(row['longitude'] + offset, row['latitude'] + offset, '',
                         ha='center', va='center', fontsize=8, color='black')
            else:
                plt.text(row['longitude'] + offset, row['latitude'] + offset, int(row['quantidade_material']),
                         ha='center', va='center', fontsize=8, color='black')

        # Colorbar
        cbar = plt.colorbar(sc)
        cbar.set_label('Quantidade de Material', rotation=270, labelpad=30)

        total_distance = df[df['distancia'] < 1000]['distancia'].head(75).sum()

        plt.xlabel('Longitude', labelpad=15)
        plt.ylabel('Latitude', labelpad=15)
        plt.title('Rota Otimizada de Entrega - Distância Total Aproximadamente: ' +
                  "{:.2f} km".format(total_distance))
        plt.grid(True)
        plt.show()
