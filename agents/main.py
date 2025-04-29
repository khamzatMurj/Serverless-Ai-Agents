from utils.utils import get_embedding






if __name__ == "__main__":
    data = get_embedding(['hamza'])
    print(len(data.data[0]['values']))




