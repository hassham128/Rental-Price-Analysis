# Hassham Malik
# Rental Price Analysis
# The purpose of this code is to create a report generator that takes an input CSV file which contains rental prices 
# in a specific housing market and generates a text file report which provides a full analysis of rental prices.

import csv

#function
def load_report(filename):
    with open(filename, newline="") as csvfile:
        #reading the file and creating diffrent lists for later use
        csv_input = csv.DictReader(csvfile)
        Address_List = []
        Neighborhood_List = []
        Price2020_List = []
        Price2021_List = []
        
        for row in  csv_input:
            Address_List.append(row['Address'])
            Neighborhood_List.append(row[' Neighborhood'])
            Price2020_List.append(row[' 2020 Rent'])
            Price2021_List.append(row[' 2021 Rent'])
        price2021_adress_dict = dict(zip(Price2021_List, Address_List))
        price_tuple = zip(Price2021_List, Price2020_List)
        
    #average, lowest, and highest rent
    ttl_rnt = 0
    for x in Price2021_List:
        price = int(x.replace(" $", ""))
        ttl_rnt += (price)
    avg_rnt = ttl_rnt/len(Price2021_List)

    high_rnt = 0
    for x in Price2021_List:
        price = int(x.replace(" $", ""))
        if price > high_rnt:
            high_rnt = price
    high_rnt_address = price2021_adress_dict.get(f" ${high_rnt}")

    low_rnt = 999999999
    for x in Price2021_List:
        price = int(x.replace(" $", ""))
        if price < low_rnt:
            low_rnt = price   
    low_rnt_address = price2021_adress_dict.get(f" ${low_rnt}")
    

    #average, lowest, highest rent
    total_change = 0 
    low_change = 999999
    high_change = 0
    change_list = []
    for a, b in price_tuple:
        price2021 = int(a.replace(" $", ""))
        price2020 = int(b.replace(" $", ""))
        diffrence = price2021 - price2020
        change_list.append(diffrence)
        total_change += diffrence
        if diffrence > high_change:
            high_change = diffrence
        if diffrence < low_change:
            low_change = diffrence
    change_address_dict = dict(zip(change_list, Address_List))
    avg_change = (total_change/len(Price2021_List))
    
    if avg_change > 0 :
        avg_change = str(f"+{avg_change:.2f}")
    high_change_address = change_address_dict.get(high_change)
    if high_change > 0 :
        high_change = str(f"+{high_change:.2f}")
    low_change_address = change_address_dict.get(low_change)
    if low_change > 0 :
        low_change = str(f"+{low_change:.2f}")    


    #neighborhood-2021 prices
    neighborhood_price2021_tuple = zip(Neighborhood_List,Price2021_List)
    neighborhood_price2021_dict = {}
    neighborhood_occurance_dict = {}
    for a, b in neighborhood_price2021_tuple:
        neighborhood = a.strip()
        
        price = int(b.replace(" $", ""))
        if neighborhood not in neighborhood_price2021_dict.keys():
            neighborhood_price2021_dict[neighborhood] = price
            neighborhood_occurance_dict[neighborhood] = 1
        else:
            neighborhood_price2021_dict[neighborhood] += price
            neighborhood_occurance_dict[neighborhood] += 1
           # print(price2021_adress_dict.get(f" ${price}"))

    
    #highest price neighborhood
    avg_neighborhood_dict = {}
    high_rnt_neighborhood_price = 0 
    for neighborhood in neighborhood_price2021_dict:

        avg_rnt_neighborhood = neighborhood_price2021_dict[neighborhood]/neighborhood_occurance_dict[neighborhood]
        avg_neighborhood_dict[avg_rnt_neighborhood] = neighborhood

        if avg_rnt_neighborhood > high_rnt_neighborhood_price:
            high_rnt_neighborhood_price = avg_rnt_neighborhood
    high_rnt_neighborhood = avg_neighborhood_dict[high_rnt_neighborhood_price]

    #lowest price neighborhood
    low_rnt_neighborhood_price = 999999999
    for neighborhood in neighborhood_price2021_dict:
        if avg_rnt_neighborhood < low_rnt_neighborhood_price:
            low_rnt_neighborhood_price = avg_rnt_neighborhood
    low_rnt_neighborhood = avg_neighborhood_dict[low_rnt_neighborhood_price]


    #neighborhood-2020 prices
    avg_neighborhood2020_dict = {}
    neighborhood_price2020_tuple = zip(Neighborhood_List,Price2020_List)
    neighborhood_price2020_dict = {}
    neighborhood_occurance_dict = {}
    neighborhood_price2020_dict_reversed = {}
    for a, b in neighborhood_price2020_tuple:
        neighborhood = a.strip()
        
        price = int(b.replace(" $", ""))
        if neighborhood not in neighborhood_price2020_dict.keys():
            neighborhood_price2020_dict[neighborhood] = price
            neighborhood_occurance_dict[neighborhood] = 1
        else:
            neighborhood_price2020_dict[neighborhood] += price
            neighborhood_occurance_dict[neighborhood] += 1

    #making a dictionary that contain the average of the 2020 rent of the neighborhoods
    for neighborhood in neighborhood_price2020_dict:
        avg_rnt_neighborhood2020 = neighborhood_price2020_dict[neighborhood]/neighborhood_occurance_dict[neighborhood]
        avg_neighborhood2020_dict[neighborhood] = avg_rnt_neighborhood2020

    #find the rent diffrence for all neighborhoods and making a dictionary
    neighborhood_rnt_change_dict = {}
    for a, b in avg_neighborhood_dict.items():
       neighborhood_rnt_change_dict[b] = a - avg_neighborhood2020_dict[b]
       if neighborhood_rnt_change_dict[b] > 0:
           neighborhood_rnt_change_dict[b] = (f"+${neighborhood_rnt_change_dict[b]:.2f}")
       else:  
            neighborhood_rnt_change_dict[b] = (f"${neighborhood_rnt_change_dict[b]:.2f}")



  
    #write the new txt file
    f = open("report.txt" , "w")
    f.write((f"Rent Report, 2020-2021\nAverage Rent: ${avg_rnt:.2f}\nHighest Rent: ${high_rnt:.2f}, {high_rnt_address}\nLowest Rent: ${low_rnt:.2f}, {low_rnt_address}\n"))
    f.write((f"Average Rent Change: ${avg_change}\nHighest Rent Change: ${high_change}, {high_change_address}\nLowest Rent Change: ${low_change}, {low_rnt_address}\n"))
    f.write((f"Least Affordable Neighborhood: {high_rnt_neighborhood} (Avg. Rent: ${high_rnt_neighborhood_price:.2f})\n"))
    f.write((f"Most Affordable Neighborhood: {low_rnt_neighborhood} (Avg. Rent: ${low_rnt_neighborhood_price:.2f})\n"))
    f.write((f"Rent Changes by Neighborhood:\n"))
    for neighborhood in neighborhood_rnt_change_dict:
        f.write(f"\t{neighborhood} ({neighborhood_rnt_change_dict[neighborhood]})\n")    

    return "report.txt file has been created."


 
#main fuction with some code for debugging
def main():
    print(load_report("sc_rent_prices.csv")) 

    #print(f"average rent is{avg_rnt},\n high rent is {high_rnt},{high_rnt_address}\n low rent is {low_rnt},{low_rnt_address}\n")
    #print(f"average change is{avg_change},\n high change is {high_change},{high_change_address}\n low change is {low_change},{low_change_address}\n")
    #print(f"High Neighborhood is {high_rnt_neighborhood} and price is {high_rnt_neighborhood_price}\n")
    #print(avg_neighborhood2020_dict)
    #print(avg_neighborhood_dict)
    #print((f"Rent Report, 2020-2021\nAverage Rent: ${avg_rnt:.2f}\nHighest Rent: ${high_rnt:.2f}, {high_rnt_address}\nLowest Rent: ${low_rnt:.2f}, {low_rnt_address}"))
    #print((f"Average Rent: ${avg_change}\nHighest Rent Change: ${high_change}, {high_change_address}\nLowest Rent Change: ${low_change}, {low_rnt_address}"))
    #print((f"Least Affordable Neighborhood: {low_rnt_neighborhood} (Avg. Rent: ${low_rnt_neighborhood_price:.2f})"))
    #print((f"Most Affordable Neighborhood: {high_rnt_neighborhood} (Avg. Rent: ${high_rnt_neighborhood_price:.2f})"))
    #print(f"RentChanges by Neighborhood:")
    #for neighborhood in neighborhood_rnt_change_dict:
    #    print(f"\t{neighborhood} ({neighborhood_rnt_change_dict[neighborhood]})")

#calls the main function
if __name__ == "__main__":
    main()