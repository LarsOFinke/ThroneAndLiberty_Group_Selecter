import sys, gui
from PyQt5.QtWidgets import QApplication


GROUPSIZE: int = 6

ROLES: dict = {
    1: "Tank",
    2: "Heal",
    3: "DPS"
}



def form_groups(tanks: list, heals: list, dps: list) -> list[list]:
    amount_tanks: int = len(tanks)
    amount_heals: int = len(heals)
    amount_dps: int = len(dps)
    player_count: int = amount_tanks + amount_heals + amount_dps
    group_list: list = []
    
    if player_count % GROUPSIZE == 0:   # All groups full
        group_count:int = int(player_count / GROUPSIZE)
        
        
        if amount_tanks % group_count == 0 and amount_heals % group_count == 0 and amount_dps % group_count == 0 and amount_tanks != 0 and amount_heals != 0: # Optimal group composition
            for i in range(group_count):
                group: list = [tanks[0], heals[0], dps[0], dps[1], dps[2], dps[3]]
                tanks.remove(tanks[0]), heals.remove(heals[0])
                
                for k in range(4):
                    dps.remove(dps[0])
                    
                group_list.append(group)


        elif amount_heals % group_count == 0 and amount_tanks > group_count:  # 1 Heal per group, more Tanks than DPS
            for i in range(group_count):
                group: list = [heals[0]]
                heals.remove(heals[0]), group.insert(0, tanks[0]), tanks.remove(tanks[0])

                for j in range(4):
                    if len(dps) != 0:
                        group.append(dps[0]), dps.remove(dps[0])
                    else:
                        group.append(tanks[0]), tanks.remove(tanks[0])  
                        
                    if len(group) == 6:
                        group_list.append(group)
                        continue
    
        
        elif amount_heals % group_count == 0 and amount_heals != 0 and amount_dps > group_count:  # 1 Heal per group, more DPS than Tanks
            missing_players: int = 4
            for i in range(group_count):
                group: list = [heals[0]]
                heals.remove(heals[0])
                
                if len(tanks) != 0:
                    group.insert(0, tanks[0]), tanks.remove(tanks[0])
                else:
                    missing_players += 1
                    
                for j in range(missing_players):
                    group.append(dps[0]), dps.remove(dps[0])   
                        
                    if len(group) == 6:
                        group_list.append(group)
                        continue
                    
                missing_players = 4
    

        elif amount_heals % group_count != 0: # Not enough Heals
            for i in range(group_count):
                group: list = []
                
                if len(heals) != 0:
                    group.append(heals[0]), heals.remove(heals[0])
                    
                    while len(group) < 6:
                        if len(tanks) != 0:
                            group.append(tanks[0]), tanks.remove(tanks[0])
                            
                        else:
                            group.append(dps[0]), dps.remove(dps[0])
                            
                    group_list.append(group)
                
                else:
                    while len(group) < 6:
                        if len(tanks) != 0:
                            group.append(tanks[0]), tanks.remove(tanks[0])
                            
                        else:
                            group.append(dps[0]), dps.remove(dps[0])
                            
                    group_list.append(group)
                    
        else:
            for i in range(group_count):
                group: list = []
                if len(tanks) != 0:
                    group.append(tanks[0]), tanks.remove(tanks[0])
                    if len(heals) != 0:
                        group.append(heals[0]), heals.remove(heals[0])
                    while len(group) < 6:
                        group.append(dps[0]), dps.remove(dps[0])
                
                elif len(heals) != 0:
                    group.append(heals[0]), heals.remove(heals[0])
                    while len(group) < 6:
                        group.append(dps[0]), dps.remove(dps[0])
                        
                else:
                    while len(group) < 6:
                        group.append(dps[0]), dps.remove(dps[0])
                group_list.append(group)
                
                


    else:   # Not all groups ful
        group_count:int = int(round(player_count / GROUPSIZE))

        if amount_tanks % group_count == 0 and amount_heals % group_count == 0: # 1 Heal and Tank each group
            for i in range(group_count-1):
                group: list = [tanks[0], heals[0], dps[0], dps[1], dps[2], dps[3]]
                tanks.remove(tanks[0]), heals.remove(heals[0])
                
                for k in range(4):
                    dps.remove(dps[0])
                    
                group_list.append(group)
                
            last_group: list = [tanks[0], heals[0]]
            for j in range(len(dps)):
                last_group.append(dps[0]), dps.remove(dps[0])
            group_list.append(last_group)
        
        
        elif amount_tanks % group_count == 0 and amount_tanks != 0:   # 1 Tank each group
            for i in range(group_count-1):
                group: list = [tanks[0]]
                tanks.remove(tanks[0])
                
                if len(heals) != 0:
                    group.append(heals[0]), heals.remove(heals[0])
                    
                    while len(group) < 6:
                        group.append(dps[0]), dps.remove(dps[0])
                    group_list.append(group)
                
                else:
                    while len(group) < 6:
                        group.append(dps[0]), dps.remove(dps[0])
                    group_list.append(group)
                    
            last_group: list = [tanks[0]]
            while True:
                if len(heals) != 0:
                    last_group.append(heals[0]), heals.remove(heals[0])
                
                elif len(dps) != 0:
                    last_group.append(dps[0]), dps.remove(dps[0])
                else:
                    break
            group_list.append(last_group)
        
        
        elif amount_heals % group_count == 0 and amount_heals != 0:   # 1 Heal each group
            print("Hier")
            for i in range(group_count-1):
                group: list = [heals[0]]
                heals.remove(heals[0])
                
                if len(tanks) != 0:
                    group.append(tanks[0]), tanks.remove(tanks[0])
                    
                    while len(group) < 6:
                        if len(dps) != 0:
                            group.append(dps[0]), dps.remove(dps[0])
                        else:
                            if len(heals) != 0:
                                group.append(heals[0]), heals.remove(heals[0])
                            elif len(tanks) != 0:
                                group.append(tanks[0]), tanks.remove(tanks[0])
                    group_list.append(group)
                    
                else:
                    while len(group) < 6:
                        group.append(dps[0]), dps.remove(dps[0])
                    group_list.append(group)

            last_group: list = [heals[0]]
            heals.remove(heals[0])
            
            if len(tanks) != 0:
                last_group.append(tanks[0]), tanks.remove(tanks[0])
                    
                while len(group) < 6:
                    last_group.append(dps[0]), dps.remove(dps[0])
                group_list.append(last_group)
                    
            else:
                while len(dps) != 0:
                    last_group.append(dps[0]), dps.remove(dps[0])
                group_list.append(last_group)
        
        
        else:
            for i in range(group_count-1):
                group: list = []
                
                if len(tanks) != 0:
                    group.append(tanks[0]), tanks.remove(tanks[0])
                
                if len(heals) != 0:
                    group.append(heals[0]), heals.remove(heals[0])
                    
                while len(group) < 6:
                    if len(dps) != 0:
                        group.append(dps[0]), dps.remove(dps[0])
                    elif len(tanks) != 0:
                        group.append(tanks[0]), tanks.remove(tanks[0])
                    elif len(heals) != 0:
                        group.append(heals[0]), heals.remove(heals[0])
                group_list.append(group)

            last_group: list = []
            while True:
                if len(tanks) != 0:
                    last_group.append(tanks[0]), tanks.remove(tanks[0])
                
                elif len(heals) != 0:
                    last_group.append(heals[0]), heals.remove(heals[0])
                
                elif len(dps) != 0:
                    last_group.append(dps[0]), dps.remove(dps[0])
                    
                else:
                    break
                
            group_list.append(last_group)
            

    return group_list




def main():
    app = QApplication(sys.argv)
    main_window = gui.MainWindow()
    main_window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
