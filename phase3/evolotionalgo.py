import random
import gene as gn
import learningothello as lo
import logging
import log
from config import *



logger = logging.getLogger('root')

class Evolotion:
    pc = 1
    pm = 0.1
    generations_len = 10
    first_population = 4
    childs_population = 4
    population = first_population + childs_population
    genes = []
    parents = []
    childs = []
    lf = None
    leage_len = 4

    def __init__(self, logfile, first_population=6, childs_population=4, generations_len=10, leage_len=4):
        Evolotion.first_population = first_population
        Evolotion.childs_population = childs_population
        Evolotion.population = Evolotion.first_population + Evolotion.childs_population
        Evolotion.lf = logfile
        Evolotion.generations_len = generations_len
        Evolotion.leage_len = leage_len

    def train(self):
        Evolotion.lf.log_gene("___________________FIRST GENERATION__________________________")
        self.make_first_generation()
        # self.get_first_generation(
        #     [
        #         [9999, [8.193, 12.752, -19.534, 3.194, 8.45], [3.924, 16.524, 8.773, -4.972, 2.956],
        #          [-9.848, 33.754, -27.689, 11.718, 10.343], [-5.585, -10.346, -10.828, -21.482, 0.499],
        #          [-43.405, 0.927, -5.153, -7.428, -16.502], [8.196, 12.37, 3.641, 27.15, 17.494]]
        #     ,    [9999, [5.476, 24.959, -10.902, 3.824, -7.932], [17.011, 6.02, 4.939, -6.592, 13.234],
        #          [2.87, 19.531, -8.925, 13.239, 2.197], [-9.284, -13.035, -19.967, -22.897, -12.818],
        #          [-37.705, -3.569, -7.321, -13.697, -21.046], [-2.108, 5.033, -10.092, 7.301, 24.421]]
        #     ,    [9999,
        #          [23.878524414062497, 4.6640625, -3.5313144531250007, -5.5511796874999995, -4.8317294921875],
        #          [-2.8823056640624998, 12.778708984375001, 14.066373046874999, -2.3212626953125,
        #           9.405774414062499],
        #          [2.812576171875, 15.0766982421875, -5.6010458984375004, 17.9369794921875, -11.9175693359375],
        #          [-16.345970703124998, -19.03784765625, -8.536880859375, -32.9982724609375, 1.50221484375],
        #          [-21.585807617187502, -2.6899414062499996, -19.5074033203125, -5.274615234375, 12.17496484375],
        #          [-8.8133212890625, -5.3022158203125, -7.752240234375, 13.8752265625, 6.7387236328124995]]
        #     ,    [9999,
        #          [23.75190576171875, 3.95980859375, -3.3605439453125006, -5.921710937499999, -4.86981103515625],
        #          [-3.22490576171875, 12.7456689453125, 14.479860351562499, -2.20916357421875, 9.40598193359375],
        #          [2.9642998046875, 14.214055175781251, -5.87243798828125, 18.17750244140625, -11.738434082031251],
        #          [-16.3371513671875, -19.03914453125, -8.890600585937499, -32.790285644531245, 2.148576171875],
        #          [-22.609244628906254, -2.1718749999999996, -18.98563623046875, -5.2202412109375, 11.7534609375],
        #          [-8.98537060546875, -5.10181982421875, -8.0271865234375, 13.9406953125, 7.95695654296875]]
        #     ,    [9999,
        #          [23.598441162109374, 3.54383203125, -3.5828491210937505, -6.428529296875, -5.320112548828124],
        #          [-3.160605224609375, 13.036381347656251, 14.25686376953125, -1.9361608886718749,
        #           9.068247802734374],
        #          [2.9763735351562497, 13.590977783203126, -6.5595686035156255, 18.651124267578126,
        #           -11.956773681640627],
        #          [-16.67764794921875, -19.1046728515625, -9.19531298828125, -32.871832275390624, 2.9033955078125],
        #          [-22.930604736328128, -1.5897001953124996, -18.700707763671875, -5.48898095703125,
        #           11.4145341796875],
        #          [-9.269644287109376, -4.905399169921875, -8.21539501953125, 14.027416015625, 8.748162841796876]]
        #     ,    [9999,
        #          [22.657382080078126, 2.3862109375, -3.26500537109375, -6.900640624999999, -6.462822021484374],
        #          [-3.4348898925781253, 13.56989599609375, 14.78027294921875, -1.3231105957031248,
        #           8.748633056640625],
        #          [2.6437739257812503, 12.393606201171874, -7.235563232421876, 18.666988037109377,
        #           -12.317625732421877],
        #          [-16.76388720703125, -18.7245703125, -10.64412158203125, -32.51873510742187, 4.6175029296875],
        #          [-23.996710693359375, -0.6091816406249997, -17.535141845703127, -5.611568847656251,
        #           11.357021484375], [-10.353141845703124, -4.115577392578125, -8.604285644531249, 13.50947265625,
        #                              10.685093017578126]]
        #     ,    [9999, [24.957562499999998, 4.493265625, -3.8078593750000005, -6.09053125, -3.4550312499999998],
        #          [-3.21425, 12.078359375, 14.042890624999998, -2.814703125, 9.64746875],
        #          [3.71853125, 14.4236875, -5.7205, 18.86775, -11.084953125000002],
        #          [-16.459218749999998, -19.701546875, -7.311484375, -33.129296874999994, 0.914765625],
        #          [-22.593375, -2.5496718749999996, -19.892125, -5.16296875, 10.984234375],
        #          [-7.7200625, -5.92784375, -7.9404531249999994, 14.9304375, 7.196359375]]
        #     ,    [9999, [16.0254384765625, 7.5451015625, -11.653328125, -2.19077734375, 1.6649267578124998],
        #          [0.15956152343749985, 14.733939453125, 11.604306640625, -3.3848896484375004, 5.9037841796875],
        #          [-3.1274257812500004, 22.7663759765625, -17.6334091796875, 15.7743271484375,
        #           -0.6183349609375011],
        #          [-11.325474609375, -14.924673828125, -10.034523437499999, -27.146452148437497, 2.25492578125],
        #          [-34.0920927734375, 0.2538378906250002, -11.6196865234375, -6.53776171875, -3.221630859375],
        #          [-0.49166894531250005, 3.7743017578124993, -2.5658281249999995, 20.92860546875,
        #           14.2402099609375]]
        #     ,    [9999, [11.4995, 15.1305, -2.5434999999999994, -4.4305, -14.1235],
        #          [2.7064999999999992, 9.1465, 14.281, -13.045499999999999, 17.06],
        #          [-3.6430000000000002, 28.128, -2.6025, 16.061, 6.617000000000001],
        #          [-12.75, -6.9350000000000005, -19.3305, -24.8125, -5.4315],
        #          [-34.394999999999996, 3.3619999999999997, -7.32, -3.2609999999999997, 7.149999999999999],
        #          [-6.7765, -3.791, -2.8160000000000003, 6.8335, 13.1385]]
        #     ,    [9999, [22.23091796875, 3.7900234375, -2.6997890625000003, -5.63890625, -5.665144531249999],
        #          [-3.56613671875, 12.76621875, 15.400171874999998, -2.20291796875, 9.38798828125],
        #          [2.60509375, 13.480824218750001, -5.27072265625, 16.86739453125, -11.786730468750001],
        #          [-15.5275859375, -18.122718749999997, -10.2684765625, -31.906464843749998, 2.8397578125],
        #          [-23.368644531250002, -1.6302031249999995, -17.72039453125, -4.7875, 12.56759375],
        #          [-10.04193359375, -3.66942578125, -8.5277109375, 12.761828125000001, 9.13730859375]]
        #     ,    [9999, [12.49013671875, 14.022890624999999, -6.246859375, -0.6816406250000004, -7.90362890625],
        #          [6.546488281249999, 9.7370390625, 10.848226562499999, -4.09156640625, 11.18125390625],
        #          [2.180828125, 16.03448046875, -6.872972656250001, 14.053019531250001, -5.14575390625],
        #          [-11.9399765625, -14.7894453125, -16.596234374999998, -26.79031640625, -4.026625],
        #          [-30.92445703125, -2.1398671874999997, -11.43483203125, -9.054515625, -3.4475234374999992],
        #          [-7.23590234375, 1.81099609375, -9.603484375, 8.947109375, 17.74962890625]]
        #     ,    [9999, [6.8345, 18.8555, -15.218, 3.509, 0.25899999999999945],
        #          [10.4675, 11.272, 6.856, -5.782, 8.095],
        #          [-3.4890000000000003, 26.6425, -18.307000000000002, 12.4785, 6.27],
        #          [-7.4345, -11.6905, -15.397499999999999, -22.1895, -6.1594999999999995],
        #          [-40.555, -1.321, -6.237, -10.5625, -18.774],
        #          [3.0439999999999996, 8.7015, -3.2255000000000003, 17.2255, 20.9575]]
        #     ,    [9999,
        #          [20.004665039062502, 4.961435546875, -3.7782485351562505, -6.865249023437499, -7.6730244140625],
        #          [-3.3089072265625, 12.7320380859375, 13.9696044921875, -1.4259086914062498, 9.23236376953125],
        #          [1.48845166015625, 13.06704638671875, -6.650375, 14.468375000000002, -10.5687509765625],
        #          [-14.9533564453125, -16.74762939453125, -11.123712402343749, -32.1196318359375, 3.405748046875],
        #          [-23.118531250000004, -1.5950229492187495, -14.56359619140625, -3.8997661132812502,
        #           12.65505517578125],
        #          [-10.215751953125, -2.3146479492187497, -8.39553857421875, 11.7486318359375, 9.78927978515625]]
        #     ,    [9999, [16.260480224609374, 7.0836074218750005, -5.8006835937500005, -7.910141601562499,
        #                 -9.546790283203125],
        #          [-1.3372458496093753, 11.39973388671875, 11.62673583984375, -2.835906494140625,
        #           6.610089111328126],
        #          [-5.5875576171875, 13.779238037109375, -2.0517297363281255, 7.011554931640625,
        #           -10.097474853515624],
        #          [-13.410561035156253, -14.53033935546875, -15.908861328124999, -30.661867431640623,
        #           0.9273466796875001],
        #          [-29.17845727539062, -3.2339047851562492, -11.230340087890625, -2.9460205078125004,
        #           9.998946777343749],
        #          [-8.139531982421875, 0.4924440917968752, -12.38556640625, 5.3511533203125, 7.244310791015625]]
        #     ,    [9999, [21.99640625, 2.3488203125, -2.8956269531250003, -6.4954023437499995, -7.117148437499999],
        #          [-3.4308750000000003, 13.84573828125, 15.11319140625, -1.095162109375, 8.766544921875],
        #          [2.147376953125, 12.681955078125, -6.953035156250001, 17.968707031250002, -12.639273437500002],
        #          [-16.51844921875, -18.277642578124997, -11.434498046875, -32.29207812499999, 4.9304296875],
        #          [-23.71801953125, -0.7289042968749996, -17.176271484375, -5.5197910156250005,
        #           12.059939453124999],
        #          [-10.980316406250001, -3.7225722656249998, -8.530021484374998, 12.83933984375, 10.612583984375]]
        #     ,    [9999,
        #          [21.628089599609375, 3.523294921875, -2.47613134765625, -5.55449609375, -6.3725344238281245],
        #          [-3.5714645996093752, 13.09987353515625, 15.61865673828125, -1.900148193359375,
        #           9.267244873046875],
        #          [2.22797802734375, 13.376008056640625, -5.346691650390625, 16.522270751953126,
        #           -12.113470947265625],
        #          [-15.466552246093748, -17.791517578125, -11.058034667968748, -31.736959228515623,
        #           3.4566630859374996],
        #          [-23.376579345703128, -1.4413046874999995, -17.267150146484376, -4.81613623046875,
        #           12.952207031250001],
        #          [-10.674587646484376, -3.256413818359375, -8.57107763671875, 12.266957031250001,
        #           9.517607177734375]]
        #     ]
        # )
        for i in range(Evolotion.generations_len):
            Evolotion.lf.log_gene("________________" + str(i) + "___SELECT_PARENTS________________________\n")
            self.select_parents()
            Evolotion.lf.log_gene("________________" + str(i) + "___RECOMBINE_____________________________")
            self.recombine()
            Evolotion.lf.log_gene("________________" + str(i) + "___MUTATE________________________________")
            self.mutate()
            Evolotion.lf.log_gene("________________" + str(i) + "___PLAY__________________________________")
            self.play()
            Evolotion.lf.log_gene("________________" + str(i) + "___GENES__________________________________")
            self.printgenes()

        Evolotion.lf.log_gene("___________________LAST_GENES__________________________________")
        self.printgenes(export=True)

        self.select_parents()
        Evolotion.lf.log_gene("___________________RECOMBINE_____________________________")
        self.recombine()
        Evolotion.lf.log_gene("___________________FINAL_GENE__________________________________")
        self.final_gene()



    def make_first_generation(self):

        for k in range(0, Evolotion.first_population):
            temp_gene = gn.Gene()
            temp_gene.random_gene()
            Evolotion.lf.log_gene(temp_gene.vector)
            logger.debug('make_first_generation - k:%s, gene:%s', k, temp_gene.vector)
            self.genes.append(temp_gene)

    def get_first_generation(self, vectors):
        for k in range(0, Evolotion.first_population):
            temp_gene = gn.Gene(vectors[k])
            Evolotion.lf.log_gene(temp_gene.vector)
            logger.debug('get_first_generation - k:%s, gene:%s', k, temp_gene.vector)
            self.genes.append(temp_gene)

    def select_parents(self):
        for k in range(0, Evolotion.childs_population):
            p1 = random.randint(0, Evolotion.first_population - 1)
            p2 = random.randint(0, Evolotion.first_population - 1)
            while p1 == p2 or self.is_repeated(p1, p2):
                p2 = random.randint(0, Evolotion.first_population - 1)
            Evolotion.parents.append([p1, p2])
            Evolotion.lf.log_gene("{" + str(p1) + "," + str(p2) + "}",nextline= False)
            logger.debug('select_parents - k:%s, F1:%s , F2:%s', k, p1, p2)

    def is_repeated(self, p1, p2):
        for k in range(0, len(Evolotion.parents)):
            if (Evolotion.parents[k][0] == p1 and Evolotion.parents[k][1] == p2) or (
                    Evolotion.parents[k][0] == p2 and Evolotion.parents[k][1] == p1):
                return True
        return False

    def recombine(self):
        for k in range(0, Evolotion.childs_population):
            p1, p2 = Evolotion.parents[k]

            if random.random() < Evolotion.pc:
                Evolotion.childs.append(gn.Gene(Evolotion.genes[p1].recombine(Evolotion.genes[p2])))

            else:
                Evolotion.childs.append(gn.Gene(Evolotion.genes[p1].recombine(Evolotion.genes[p1])))
            Evolotion.lf.log_gene(str(p1) + "," + str(p2) + " : " + str(Evolotion.childs[k].vector))
            logger.debug('recombine - k:%s, F1:%s , F2:%s', k, p1, p2)

    def mutate(self):
        for k in range(0, Evolotion.childs_population):
            if random.random() < Evolotion.pm:
                Evolotion.childs[k].mutate()
                Evolotion.lf.log_gene(Evolotion.childs[k].vector)
                logger.debug('mutate - k:%s, gene:%s', k, Evolotion.childs[k].vector)

    def play(self):
        Evolotion.genes.extend(Evolotion.childs)
        Evolotion.parents = []
        Evolotion.childs = []
        logger.debug('play - reset scores')
        for i in range(Evolotion.population):
            Evolotion.genes[i].score = 0
        for k in range(Evolotion.leage_len):
            random.shuffle(Evolotion.genes)
            for i in range(0, Evolotion.population, 2):
                logger.debug('play - i:%s, gene1:%s --- gene2:%s', i, Evolotion.genes[i].vector,
                             Evolotion.genes[i + 1].vector)
                game1 = lo.learningOthello(Evolotion.genes[i].vector, Evolotion.genes[i + 1].vector)
                res1 = game1.run()
                game2 = lo.learningOthello(Evolotion.genes[i + 1].vector, Evolotion.genes[i].vector)
                res2 = game2.run()
                if res1[0] + res2[1] > res1[1] + res2[0]:
                    Evolotion.genes[i].score += 3
                    Evolotion.lf.log_gene(
                        str(i) + "," + str(i + 1) + "  G1:" + str(res1[0]) + " " + str(res1[1]) + " & G2:" + str(
                            res2[1]) + " " + str(res2[0]) + " Winner" + str(i))
                elif res1[0] + res2[1] < res1[1] + res2[0]:
                    Evolotion.genes[i + 1].score += 3
                    Evolotion.lf.log_gene(
                        str(i) + "," + str(i + 1) + "  G1:" + str(res1[0]) + " " + str(res1[1]) + " & G2:" + str(
                            res2[1]) + " " + str(res2[0]) + " Winner" + str(i + 1))
                else:
                    Evolotion.genes[i].score += 1
                    Evolotion.genes[i + 1].score += 1
                    Evolotion.lf.log_gene(str(i) + "," + str(i + 1) + "  G1:" + str(res1[0]) + " " + str(res1[1]) +
                                          " & G2:" + str(res2[1]) + " " + str(res2[0]) + " Winner" + "===")

        Evolotion.genes.sort(key=lambda x: x.score, reverse=True)
        temp = int(round(Evolotion.first_population / 4, 0))
        next_generation = Evolotion.genes[0:Evolotion.first_population - temp]
        Evolotion.genes = Evolotion.genes[Evolotion.first_population - temp:]
        next_generation.extend(random.sample(Evolotion.genes, temp))
        Evolotion.genes = next_generation

    def printgenes(self,export=False):
        if not export:
            for i in range(len(Evolotion.genes)):
                Evolotion.lf.log_gene(str(i) + " : " + str(Evolotion.genes[i].vector))
        else:
            Evolotion.lf.log_gene( "        [ " + str(Evolotion.genes[0].vector))
            for i in range(1,len(Evolotion.genes)):
                Evolotion.lf.log_gene(" , " + str(Evolotion.genes[i].vector  ),time=False)
            Evolotion.lf.log_gene(" ] ",time=False)

    def final_gene(self):
        Evolotion.genes.extend(Evolotion.childs)
        Evolotion.parents = []
        Evolotion.childs = []
        logger.debug('finalgene - reset scores')
        for i in range(Evolotion.population):
            Evolotion.genes[i].score = 0
        for k in range(Evolotion.population):
            for i in range(k+1, Evolotion.population):
                logger.debug('play - k:%s ,i:%s, gene1:%s --- gene2:%s',k, i, Evolotion.genes[k].vector,
                             Evolotion.genes[i].vector)
                game1 = lo.learningOthello(Evolotion.genes[k].vector, Evolotion.genes[i].vector)
                res1 = game1.run()
                game2 = lo.learningOthello(Evolotion.genes[i].vector, Evolotion.genes[k].vector)
                res2 = game2.run()
                if res1[0] + res2[1] > res1[1] + res2[0]:
                    Evolotion.genes[k].score += 3
                    Evolotion.lf.log_gene(
                        str(k) + "," + str(i) + "  G1:" + str(res1[0]) + " " + str(res1[1]) + " & G2:" + str(
                            res2[1]) + " " + str(res2[0]) + " Winner" + str(k))
                elif res1[0] + res2[1] < res1[1] + res2[0]:
                    Evolotion.genes[i].score += 3
                    Evolotion.lf.log_gene(
                        str(k) + "," + str(i) + "  G1:" + str(res1[0]) + " " + str(res1[1]) + " & G2:" + str(
                            res2[1]) + " " + str(res2[0]) + " Winner" + str(i))
                else:
                    Evolotion.genes[k].score += 1
                    Evolotion.genes[i].score += 1
                    Evolotion.lf.log_gene(str(k) + "," + str(i) + "  G1:" + str(res1[0]) + " " + str(res1[1]) +
                                          " & G2:" + str(res2[1]) + " " + str(res2[0]) + " Winner" + "===")

        logger.debug("final scores")
        for i in range(Evolotion.population):
            print(i,str(Evolotion.genes[i].score))
        Evolotion.genes.sort(key=lambda x: x.score, reverse=True)
        Evolotion.lf.log_gene("BEST GENE IS : ")
        Evolotion.lf.log_gene(str(Evolotion.genes[0].vector) , time=False)
        return Evolotion.genes[0].vector

def play_with_best_gene():

    game1 = lo.learningOthello(player1vec=BESTGENE)
    res1 = game1.run()
    game2 = lo.learningOthello(player2vec=BESTGENE)
    res2 = game2.run()
    print(res1, "---", res2)



def main():
    # pop = 20
    # gen_len = 1
    # lf = log.logfile("pop_" + str(pop) + "_generation_" + str(gen_len) + "_log.txt")
    # e = Evolotion(logfile=lf, first_population=16, childs_population=24, generations_len=gen_len)
    # e.train()

    play_with_best_gene()


if __name__ == '__main__':
    main()

#(36, 28) --- (14, 50) with depth 10
#(43, 20) --- (22, 42) with depth 8
#(37, 27) --- (17, 47) with depth 5