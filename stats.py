import csv
import os


class Stats:
    def show_score_stats(self, file_name):
        csv_path = os.path.join("scoresheet", file_name)
        self.get_play_count(csv_path)
        self.calc_avarage(csv_path)

    def calc_avarage(self, csv_path):
        """レベルごとの平均点を計算し、出力する"""
        with open(csv_path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f, delimiter=",")
            level_score_dict = {} # 辞書型
            level_list = []
            for row in r:
                music_level = int(row["楽曲レベル"])
                score = int(row["ハイスコア"])
                if music_level not in level_list:
                    level_score_dict[music_level] = {"譜面数": 1, "スコア合計": score}
                    level_list.append(music_level)
                else:
                    target_level_scores = level_score_dict[music_level]
                    target_level_scores["譜面数"] += 1
                    target_level_scores["スコア合計"] += score
                    level_score_dict[music_level] = target_level_scores
            for level, score in level_score_dict.items():
                level_score_dict[level]["平均スコア"] = score["スコア合計"] / score["譜面数"]

            print(sorted(level_score_dict.items()))


    def get_play_count(self, csv_path):
        """プレーした譜面の合計回数（投入クレジット数ではない）を出力する"""
        with open(csv_path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f, delimiter=",")
            play_count = 0
            for row in r:
                play_count += int(row["プレー回数"])
            print("譜面プレー回数：{play_count}".format(play_count=play_count))


stats = Stats()
files = os.listdir("scoresheet")
files_file = [f for f in files if os.path.isfile(os.path.join("scoresheet", f))]

for file in files_file:
    stats.show_score_stats(file)

