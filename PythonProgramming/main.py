class Solution:
    def __init__(self) -> None:
        self.chest = {
            "42": "It is the Answer to Life the Universe and Everything.",
            "666": "If you would be a real seeker after truth, it is necessary that at least once in your life you doubt, as far as possible, all things.",
            "8": "It is wrong always, everywhere and for everyone, to believe anything upon insufficient evidence.",
            "13": "The Truth is in the Heart.",
            "0": "Freedom is secured not by the fulfilling of ones desires, but by the removal of desire.",
            "9": "The unexamined life is not worth living.",
            "76": "Life is a series of natural and spontaneous changes.",
            "70": "God is dead! He remains dead! And we have killed him.",
        }

    def sort(self) -> "Solution":
        self.keys = list(self.chest.keys())

        for i in range(len(self.keys)):
            for j in range(i, len(self.keys)):
                if int(self.keys[i]) > int(self.keys[j]):
                    self.keys[i], self.keys[j] = self.keys[j], self.keys[i]

        duplicate_dict = dict()
        for key in self.keys:
            duplicate_dict[key] = self.chest[key]

        self.chest = duplicate_dict
        return self

    def concatenate_values(self) -> "Solution":
        self.ordered_values = [
            self.keys[0],
            self.keys[1],
            self.keys[-1],
            self.keys[-2],
        ]
        self.concatenated_string = ""

        for key in self.ordered_values:
            self.concatenated_string += self.chest.get(key) + " "
        return self

    def get_filtered_concatenated_string(self) -> "Solution":
        self.new_string = ""

        for val in self.concatenated_string.split():
            self.new_string += val[0] + val[-1]
        return self

    def get_character_count(self) -> "Solution":
        self.character_dict = dict()

        for i in self.new_string.lower():
            if value := self.character_dict.get(i):
                self.character_dict[i] = value + 1
            else:
                self.character_dict[i] = 1

        self.character_dict = sorted(list(self.character_dict.values()), reverse=True)
        self.character_dict = self.character_dict[:5]
        return self

    def treasure(self) -> None:
        keys_list = [52, 51, 61, 71, 56]

        sum_list = [i + int(j) for i, j in zip(self.character_dict, keys_list)]
        print("tressure: ", end="")
        print(*[chr(i) for i in sum_list], sep="")


if __name__ == "__main__":
    (
        Solution()
        .sort()
        .concatenate_values()
        .get_filtered_concatenated_string()
        .get_character_count()
        .treasure()
    )
