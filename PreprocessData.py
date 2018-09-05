
from pymongo import MongoClient

path_JSON = ""
category_indices_file = "/Users/shatha/Downloads/instagram-dataset/category-subCategory/categories_indices"
sub_category_indices_file = "/Users/shatha/Downloads/instagram-dataset/category-subCategory/subcategories_indices"
style_indices_file = "/Users/shatha/Downloads/instagram-dataset/category-subCategory/style_indices"
attributes_file = "/Users/shatha/Downloads/instagram-dataset/attributes-classifications/all_attributes"

community_clothing_training_singleValues_file = "/Users/shatha/Downloads/instagram-dataset/analysis/community_clothing_training_singleValues"
community_clothing_testing_singleValues_file = "/Users/shatha/Downloads/instagram-dataset/analysis/community_clothing_testing_singleValues"

class PreprocessData(object):

    def readCategoryIndices(self):
        dict_categories = {}
        with open(category_indices_file, "r") as file_category_indices:
            for line in file_category_indices:
                dict_categories[line.split(",")[0]] = line.split(",")[1]
        return dict_categories

    def readStyleIndices(self):
        dict_styles = {}
        with open(style_indices_file, "r") as file_style_indices:
            for line in file_style_indices:
                dict_styles[line.split(",")[0]] = line.split(",")[1]
        return dict_styles

    def readSubCategoryIndices(self):
        dict_sub_categories = {}
        counter = 0
        with open(sub_category_indices_file, "r") as file_sub_category_indices:
            for line in file_sub_category_indices:
                if counter < 1:
                    counter += 1
                    continue
                dict_sub_categories[line.split(",")[0]] = line.split(",")[1]
        return dict_sub_categories

    def readAttributes(self):
        dict_attributes = {}
        with open(attributes_file, "r") as file_attributes_indices:
            for line in file_attributes_indices:
                dict_attributes[line.split(",")[0]] = line.split(",")[1]
        return dict_attributes

    def __init__(self):
        self.dict_categories = self.readCategoryIndices()
        self.dict_sub_categories = self.readSubCategoryIndices()
        self.dict_attributes = self.readAttributes()
        self.dict_styles = self.readStyleIndices()

    def readImagesTextInfo(self):
        data = []
        client = MongoClient('shatha2.it.kth.se', 27017)
        db = client['annotatorwebapp']
        collection = db.imageidtextanalysisdata

        counter = 0
        for data in collection.find():
            image_id = data["_id"]
            image_styles = data["styles"]
            image_links = data["links"]
            item_category = data["item_category"]
            image_hashtags = data["hashtags"]
            image_patterns = data["patterns"]
            image_materials = data["materials"]
            image_brands = data["brands"]
            image_sub_categories = data["item_sub_category"]

            item_category_count = item_category["count"]
            item_category_data = item_category["data"]

            item_patterns_count = image_patterns["count"]
            item_patterns_data = image_patterns["data"]

            item_materials_count = image_materials["count"]
            item_materials_data = image_materials["data"]

            item_subCategory_count = image_sub_categories["count"]
            item_subCategory_data = image_sub_categories["data"]

            # Read image categories and save images with their categories
            lstCategories = []
            category_1 = item_category_data[0].split(":")[0]
            category_2 = item_category_data[1].split(":")[0]
            category_3 = item_category_data[2].split(":")[0]
            category_4 = item_category_data[3].split(":")[0]
            # get image's category id to save in the file
            category1_id = self.dict_categories.get(category_1)
            if(category1_id == None):
                print("category 1")
                print(category_1)
                print(category1_id)
            category2_id = self.dict_categories.get(category_2)
            if(category2_id == None):
                print("category 2")
                print(category_2)
                print(category2_id)
            category3_id = self.dict_categories.get(category_3)
            if(category3_id == None):
                print("category 3")
                print(category_3)
                print(category3_id)
            category4_id = self.dict_categories.get(category_4)
            if(category4_id == None):
                print("category 4")
                print(category_4)
                print(category4_id)

            # Read image sub-categories and save them
            sub_category_1 = item_subCategory_data[0].split(":")[0]
            sub_category_2 = item_subCategory_data[1].split(":")[0]
            sub_category_3 = item_subCategory_data[2].split(":")[0]
            sub_category_4 = item_subCategory_data[3].split(":")[0]
            # get image's sub category id to save in the file
            sub_category1_id = self.dict_sub_categories.get(sub_category_1)
            if sub_category1_id == None:
                print("id of sub category 1")
                print(sub_category_1)
                print(sub_category1_id)
            sub_category2_id = self.dict_sub_categories.get(sub_category_2)
            if sub_category2_id == None:
                print("id of sub category 2")
                print(sub_category_2)
                print(sub_category2_id)
            sub_category3_id = self.dict_sub_categories.get(sub_category_3)
            if sub_category3_id == None:
                print("id of sub category 3")
                print(sub_category_3)
                print(sub_category3_id)
            sub_category4_id = self.dict_sub_categories.get(sub_category_4)
            if sub_category4_id == None:
                print("id of sub category 4")
                print(sub_category_4)
                print(sub_category4_id)


            # Read image attributes and save them
            attribute_1 = item_materials_data[0].split(":")[0]
            attribute_2 = item_materials_data[1].split(":")[0]
            attribute_3 = item_materials_data[2].split(":")[0]
            attribute_4 = item_materials_data[3].split(":")[0]
            attribute_5 = item_patterns_data[0].split(":")[0]
            attribute_6 = item_patterns_data[1].split(":")[0]
            attribute_7 = item_patterns_data[2].split(":")[0]
            attribute_8 = item_patterns_data[3].split(":")[0]
            # get indices of attributes to save them in files
            attribute1_id = self.dict_attributes.get(attribute_1)
            if attribute1_id == None:
                print("id of attribute")
                print(attribute_1)
                print(attribute1_id)
            attribute2_id = self.dict_attributes.get(attribute_2)
            if attribute2_id == None:
                print("id of attribute")
                print(attribute_2)
                print(attribute2_id)
            attribute3_id = self.dict_attributes.get(attribute_3)
            if attribute3_id == None:
                print("id of attribute")
                print(attribute_3)
                print(attribute3_id)
            attribute4_id = self.dict_attributes.get(attribute_4)
            if attribute4_id == None:
                print("id of attribute")
                print(attribute_4)
                print(attribute4_id)
            attribute5_id = self.dict_attributes.get(attribute_5)
            if attribute5_id == None:
                print("id of attribute")
                print(attribute_5)
                print(attribute5_id)
            attribute6_id = self.dict_attributes.get(attribute_6)
            if attribute6_id == None:
                print("id of attribute")
                print(attribute_6)
                print(attribute6_id)
            attribute7_id = self.dict_attributes.get(attribute_7)
            if attribute7_id == None:
                print("id of attribute")
                print(attribute_7)
                print(attribute7_id)
            attribute8_id = self.dict_attributes.get(attribute_8)
            if attribute8_id == None:
                print("id of attribute")
                print(attribute_8)
                print(attribute8_id)

        #break
            # Read image styles and save them
            style_1 = image_styles["data"][0].split(":")[0]
            style1_id = self.dict_styles.get(style_1)
            if style1_id == None:
                print("id of style")
                print(style_1)
                print(style1_id)
            style_2 = image_styles["data"][1].split(":")[0]
            style2_id = self.dict_styles.get(style_2)
            if style2_id == None:
                print("id of style")
                print(style_2)
                print(style2_id)
            style_3 = image_styles["data"][2].split(":")[0]
            style3_id = self.dict_styles.get(style_3)
            if style3_id == None:
                print("id of style")
                print(style_3)
                print(style3_id)
            style_4 = image_styles["data"][2].split(":")[0]
            style4_id = self.dict_styles.get(style_4)
            if style4_id == None:
                print("id of style")
                print(style_4)
                print(style4_id)

            subcategory_val = -1
            material_val = -1
            pattern_val = -1
            style_val = -1

            if(sub_category1_id != None):
                subcategory_val = sub_category1_id.strip()
                material_val = attribute1_id.strip()
                pattern_val = attribute5_id.strip()
                style_val = style1_id.strip()
            else:
                subcategory_val = sub_category2_id.strip()
                material_val = attribute2_id.strip()
                pattern_val = attribute6_id.strip()
                style_val = style2_id.strip()

            if counter <= 58454:
                with open(community_clothing_training_singleValues_file, "a") as file_community_training:
                    file_community_training.write(subcategory_val + "   " + material_val  + "  " + pattern_val  + "  " + style_val )
                    file_community_training.write("\n")
            else:
                with open(community_clothing_testing_singleValues_file, "a") as file_community_testing:
                    file_community_testing.write(subcategory_val + "   " + material_val  + "  " + pattern_val  + "  " + style_val )
                    file_community_testing.write("\n")

            counter += 1

        #with open(list_images_styles, "a") as file_image_styles:
        #    file_image_styles.write(image_id + "," + style1_id.strip())
         #   file_image_styles.write("\n")

        #with open(list_images_sub_categories, "a") as file_image_sub_categories:
        #    file_image_sub_categories.write(image_id + "," + sub_category1_id.strip() + "," + sub_category2_id.strip() + "," + sub_category3_id.strip() + "," + sub_category4_id.strip())
        #    file_image_sub_categories.write("\n")

        #with open(list_images_attributes, "a") as file_image_attributes:
        #    file_image_attributes.write(image_id + "," + attribute1_id.strip() + "," + attribute2_id.strip() + "," + attribute3_id.strip() + "," + attribute4_id.strip() +
        #                               "," + attribute5_id.strip() + "," + attribute6_id.strip() + "," + attribute7_id.strip() + "," + attribute8_id.strip())
        #    file_image_attributes.write("\n")


obj = PreprocessData()
obj.readImagesTextInfo()