class ConfigClass:
    def __init__(self):
        self.corpusPath = 'C:\\Users\Chana\Documents\SearchEngine\Data'
        #self.corpusPath = 'C:\\Users\Chana\Documents\SearchEngine\Search_Engine-master'
        # self.corpusPath = "C:\\Users\elitm\PycharmProjects\Search_Engine-maste\Data"
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.toStem = False

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
