import spacy
import psycopg2
import collections

class FoodLabel:



    def __init__(self, new_label):


        self.nlp = spacy.load('en_core_web_sm')


        #self.mapping = collections.defaultdict()

        self.label = new_label
        self.__processLabel()
        return

    def __processLabel (self):
        doc = self.nlp(self.label)
        self.root = '(unknown)'
        for chunk in doc.noun_chunks:
            self.root = chunk.root.text

        # basic attribution (more to be done by ML)
        #__TODO: the lists will go into the database
        self.foodType = {}
        self.__loadCategories()
        for key in self.categories.keys():
            if self.__containsWords(self.label, self.categories[key]):
                self.foodType[key] = 'Y'
            else:
                self.foodType[key] = 'U'




    def __containsWords(self, sentence, wordList):
        for word in wordList:
            if word.lower() in sentence.lower():
                return True
        return False

    def __loadCategories(self):
        connection = psycopg2.connect(host='', database='food', user='admin', password='')
        cursor = connection.cursor()
        cursor.execute('select category, categorykeyword from foodCategories c, foodCategoryKeywords k where c.id = k.categoryid')
        rows = cursor.fetchall()
        self.categories = {}

        for row in rows:
            value = self.categories.get(row[0], [])
            value.append(row[1])
            self.categories[row[0]] = value


    def printFoodType(self):
        print("{} ({})".format(self.label, lbl.root.upper()))
        for key in self.categories.keys():
            if self.__containsWords(self.label, self.categories[key]):
                print ("\t is {}".format(key))

    def checkFoodType(self, key):
        if lbl.foodType[key] == 'Y':
            print("{} is {}".format(self.label, key))

    def getRoot(self):
        return lbl.root

############## end of class ##########################################

lbl = FoodLabel("Great New Jersey chicken nuggests")


print("Product is ", lbl.getRoot())
lbl.printFoodType()

lbl.checkFoodType('meat')

lbl = FoodLabel("Bio milk chocolate")

print("Product is ", lbl.root)
lbl.printFoodType()

lbl = FoodLabel("KitKat")
lbl.printFoodType()

lbl = FoodLabel("Smirnoff Vodka")
lbl.printFoodType()
