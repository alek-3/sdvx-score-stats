import csv
import os

import datetime


class AverageScores:
    record_date = ''
    averages = []

    def __init__(self, file_name):
        csv_path = os.path.join("scoresheet", file_name)
        record_date = self.filename_to_date(file_name)
        averages = self.calc_avarage(csv_path)

    def calc_avarage(self, csv_path):
        """レベルごとの平均点を計算し、出力する"""
        with open(csv_path, "r", encoding="utf-8") as f:
            r = csv.DictReader(f, delimiter=",")
            level_score_dict = {}  # 辞書型
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
            print(sorted(level_score_dict.items())[16][1]['平均スコア'])
            return sorted(level_score_dict.items())

    def filename_to_date(self, file_name):
        """日付を表す文字列を日付形式に変換する？(例:'score20180616')"""
        date_str = file_name[5:13]
        record_date = datetime.datetime.strptime(date_str, '%Y%m%d')
        return record_date.date()
