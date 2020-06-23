import pickle
import matplotlib.pyplot as plt

camp_names = ["Mahama", "Nduta", "Nyarugusu", "Nakivale", "Lusenda"]
g_sizes = ["1", "5", "100", "lognormal_2_0.5", "normal_5_1.25"]
RUNS = 5

# for i in g_sizes:
#     runs = []
#     for j in range(RUNS):
#         runs.append(pickle.load(open("error_rel_" + i + "_" + str(j) + ".p", "rb")))
#
#     for name in camp_names:
#         run0 = runs[0][name + "_err"]
#         run1 = runs[1][name + "_err"]
#         run2 = runs[2][name + "_err"]
#         run3 = runs[3][name + "_err"]
#         run4 = runs[4][name + "_err"]
#
#         zipped = list(zip(run0, run1, run2, run3, run4))
#         average = []
#         for j in range(len(zipped)):
#             av = sum(zipped[j]) / len(zipped[j])
#             average.append(av)
#
#         plt.title("Average error for " + str(RUNS) + " runs of " + name + " with group size = " + i)
#         plt.plot(average)
#         plt.savefig("plots/" + name + "_error_abs_average" + i + ".png", dpi=300)
#         plt.clf()
#

for name in camp_names:
    for i in g_sizes:
        runs = []
        for j in range(RUNS):
            runs.append(pickle.load(open("error_rel_" + i + "_" + str(j) + ".p", "rb")))

        run0 = runs[0][name + "_err"]
        run1 = runs[1][name + "_err"]
        run2 = runs[2][name + "_err"]
        run3 = runs[3][name + "_err"]
        run4 = runs[4][name + "_err"]

        zipped = list(zip(run0, run1, run2, run3, run4))
        average = []
        for j in range(len(zipped)):
            av = sum(zipped[j]) / len(zipped[j])
            average.append(av)

        plt.plot(average, label="group size " + i)
    plt.title("Average error for " + str(RUNS) + " runs of " + name)
    plt.legend()
    plt.savefig("plots/" + name + "_error_rel_average_comb.png", dpi=300)
    plt.clf()
