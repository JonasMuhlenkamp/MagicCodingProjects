from optimizer.set_list_generator import update_set_list
from optimizer.sheet_organizer import organize_sheet

def main(option, filepath):

    if option == "list":

        update_set_list("C:\\Users\\Crit Hit Gaming\\Desktop\\PullSheetOptimizer\\CSVFiles\\ordered_set_list.csv")
    
    elif option == "optimize":

        organize_sheet("C:\\Users\\Crit Hit Gaming\\Desktop\\PullSheetOptimizer\\CSVFiles\\ordered_set_list.csv", filepath, "C:\\Users\\Crit Hit Gaming\\Desktop\\PullSheetOptimizer\\CSVFiles\\PullSheet.csv")