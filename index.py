from models.dataset import Dataset
from algorithms.wpfiApriori import wPFIApriori

dataset = Dataset("./data/connects.txt", 10000)

apriori = wPFIApriori(
    dataset.get_dataset(),
    dataset.get_items(),
    0.2 * len(dataset.get_dataset()),
    0.6,
    0.6,
)

size_one_wpfi = apriori.find_size_one_wPFI()
result = apriori.wPFI_apriori_mining()
print(result)
