from model.school_model import School, Faculty, Department, Program, Level


# This function is used to initialize some values into the School, Faculty, Department, Program and Level tables before coding commences

def InitTables(session):

    # Inputs some data when initializing the database
    session.add_all([School('University of Lagos'), School('University of Ibadan'), School('University of Ife')])
    session.add_all([Faculty('Engineering', 1), Faculty('Sciences', 1), Faculty('Law', 1), Faculty('Social Science', 1)])
    session.add_all([Department('Chemical', 1), Department('Electrical', 1), Department('Biology',2)])
    session.add_all([Program('Petroleum & Gas', 1), Program('Chemical', 1), Program('Computer', 2), Program('Electrical', 2), Program('Biology', 3)])
    session.add_all([Level(100), Level(200), Level(300), Level(400), Level(500)])
    session.commit()
    session.close()
