from src.carbon_manipulation.surfaces import rectsheet

#from carbon-structures.examples.sample import add, divide, make_array

def test_graphene_gen():
    # test smallest sheet
    sheet33 = rectsheet.RectangularSheet(3,3)
    assert len(sheet33.generate_coords()) == 6