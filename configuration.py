class ConfigClass:

    def __init__(self):
        # self.corpusPath = 'C:\\Users\Chana\Documents\SearchEngine\Data'
        self.corpusPath = "C:\\Users\elitm\PycharmProjects\Search_Engine-maste\Data"
        self.savedFileMainFolder = "C:\\Users\elitm\PycharmProjects\Search_Engine-maste\output_path"
        # self.savedFileMainFolder = "C:\\Users\Chana\Documents\SearchEngine\Search_Engine-master\output_path"
        self.saveFilesWithStem = self.savedFileMainFolder + "\\WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "\\WithoutStem"
        self.toStem = False

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
