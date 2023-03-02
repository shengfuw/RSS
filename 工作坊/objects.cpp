#include <iostream>
#include <math.h> 
#include <string>
#include <vector>
#include <random>
#include <fstream>
#include <tuple>
#include "objects.h"
using namespace std;

// ID -> 正的為 citizen, 負的 LEO
// activeType -> -1: "Never active"; 0: "Conditionally active"; 1: "Always active"
// status -> -1:out of lattice; 0:unoccupied ; 1:LEO ; 2:citizen(quiescent) ; 3:citizen(active); 4 citizen(never acitve); 5 citizen(in jail)

Lattice::Lattice(int size): size(size){
    map = new int*[size];
    IDmap = new int*[size];
    for(int i = 0; i < size; i++){
        map[i] = new int[size];
        IDmap[i] = new int[size];
        for(int j = 0; j < size; j++){
            map[i][j] = 0;
            IDmap[i][j] = 0;
            unoccupied_position_index.push_back(i*size+j);
        }  
    }
    day = -2;
}
Lattice::~Lattice(){
    for(int i = 0; i < size; i++) {
        delete[] map[i];
        delete[] IDmap[i];
    }
    for(int i = 0; i < citizen_num; i++)
        delete[] citizens[i];
    for(int i = 0; i < LEO_num; i++)
        delete[] LEOs[i];
    delete[] map;
    delete[] IDmap;
    delete[] IDs;
    delete[] citizens;
    delete[] LEOs;
}
void Lattice::place_agents(float citizen_density, int LEO_num, float alwaysActive, float neverActive, string functionForm, int citizen_vision, int LEO_vsion, int jailMAX){
    day = -1;
    this->citizen_density = citizen_density;
    this->LEO_num = LEO_num;
    this->citizen_num = size * size * citizen_density;
    this->alwaysActive = alwaysActive;
    this->neverActive = neverActive;
    this->legitimacy = 1 - (2 * alwaysActive / (neverActive * (1 - neverActive)));
    this->threshold = (2 * alwaysActive) / (1 - neverActive);
    this->functionForm = functionForm;
    this->citizen_vision = citizen_vision;
    this->LEO_vision = LEO_vsion;
    this->jailMAX = jailMAX;
    citizens = new Citizen*[citizen_num];
    LEOs = new LEO*[LEO_num];
    IDs = new int[citizen_num+LEO_num];
    alwaysActive_start_index = citizen_num * alwaysActive;
    neverActive_end_index = citizen_num * (alwaysActive + neverActive);

    random_device rd;
    mt19937 seed(rd()); // or seed(827)
    shuffle(unoccupied_position_index.begin(), unoccupied_position_index.end(), seed);
    vector<int> citizen_positions_index, LEO_positions_index;
    IDs = new int[citizen_num + LEO_num];
    for(int i = 0; i < citizen_num + LEO_num; i++){
        if(i < citizen_num){
            citizen_positions_index.push_back(unoccupied_position_index[i]);
            IDs[i] = i;
        }
        else{
            LEO_positions_index.push_back(unoccupied_position_index[i]);
            IDs[i] = -1 * (i - citizen_num);
        }
    }
    for(int i = 0; i < citizen_num; i++){
        int x = citizen_positions_index[i] / size, y = citizen_positions_index[i] % size;
        // ID -> 正的為 citizen, 負的 LEO
        // activeType -> -1: "Never active"; 0: "Conditionally active"; 1: "Always active"
        if(i < alwaysActive_start_index)
            citizens[i] = new Citizen(this, i, x, y, 1); 
        else if(i < neverActive_end_index)
            citizens[i] = new Citizen(this, i, x, y, -1);
        else
            citizens[i] = new Citizen(this, i, x, y, 0);
    }
    for(int i = 0; i < LEO_num; i++){
        int x = LEO_positions_index[i] / size, y = LEO_positions_index[i] % size;
        LEOs[i] = new LEO(this, -1 * i, x, y);
    }
}
void Lattice::set_up_citizens(){
    day = 0;
    for(int i = neverActive_end_index; i < citizen_num; i++)
        citizens[i]->set_perceivedNetRisk(this, functionForm);
    for(int i = 0; i < alwaysActive_start_index; i++)
        citizens[i]->toJail(this);
}
int Lattice::get_status(int x, int y) const{
    if(x >= 0 & y >= 0 & x < size & y < size)
        return map[x][y];
    else
        return -1;
}
int Lattice::get_ID(int x, int y) const{
    if(x >= 0 & y >= 0 & x < size & y < size)
        return IDmap[x][y];
    else
        return -1;
}
void Lattice::set_status_ID(int x, int y, int status, int ID){
    if(x >= 0 & y >= 0 & x < size & y < size){
        int position_index = x * size + y, old_status = map[x][y];
        if((old_status >= 1 & old_status <= 2) & (status == 0 | status == 5))
            unoccupied_position_index.push_back(position_index);
        if((old_status == 0 | old_status == 5) & (status >= 1 & status <= 4))
            unoccupied_position_index.erase(remove(unoccupied_position_index.begin(), unoccupied_position_index.end(), position_index), unoccupied_position_index.end());

        map[x][y] = status;
        IDmap[x][y] = ID;
    }
}
void Lattice::switch_status(int x1, int y1, int x2, int y2, int ID1, int ID2){
    int temp_status = get_status(x1, y1);
    set_status_ID(x1, y1, get_status(x2, y2), ID2);
    set_status_ID(x2, y2, temp_status, ID1);
}
vector<vector<int> > Lattice::get_status_in_vision(int x, int y, int vision) const{
    vector<vector<int> > positions_in_vision;
    for(int i = -vision; i <= vision; i++){
        for(int j = -vision; j <= vision; j++){
            if(abs(i) + abs(j) <= vision * 1.5){
                int status = get_status(x+i, y+j);
                if(status > 0 & get_distant(x+i, y+j, x, y) <= (static_cast<float>(vision) + 0.25)){
                    vector<int> position;
                    position.push_back(x); position.push_back(y); position.push_back(status);
                    positions_in_vision.push_back(position);
                }
            }
        }
    }
    return positions_in_vision;
}
// void Lattice::each_time_step(){

// }
void Lattice::get_info(ofstream& Myfile) const{
    if(day != -1){
        int inactive_num = 0, active_num = 0, inJail_num = 0;
        for(int i = 0; i < size; i++){
            for(int j = 0; j < size; j++){
                switch(map[i][j]){
                case 2:
                    inactive_num++; break;
                case 3:
                    active_num++; break;
                case 4:
                    inactive_num++; break;
                case 5:
                    inJail_num++; break;
                default:
                    break;
                }
            }
        }
        Myfile << day << "," << size << "," << LEO_num+citizen_num << "," << LEO_num << "," << citizen_num << "," << inactive_num << "," << active_num << "," << inJail_num << "," << citizen_num*9 << "," << static_cast<float>(LEO_num) / (static_cast<float>(citizen_num) / 1000.0) << "," << citizen_density << "," << alwaysActive  << "," << neverActive << "," << 1-alwaysActive-neverActive << "\n";
    }
}
void Lattice::display(ofstream& Myfile) const{
    Myfile << day << '\n';
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            Myfile << map[i][j];
            if(j != size-1)
                Myfile << ',';
        }
        Myfile << '\n';
    }
}

Agent::Agent(int ID, int x, int y): ID(ID){
    position_x = x;
    position_y = y;
}
void Agent::move(Lattice* lattice){
    vector<vector<int> > neighbor_positions;
    for(int i = -1; i <= 1; i++){
        for(int j = -1; j <= 1; j++){
            if((i != 0 | j != 0) & (lattice->get_status(position_x+i, position_y+j) != -1)){
                vector<int> n; n.push_back(position_x+i); n.push_back(position_y+j);
                neighbor_positions.push_back(n);
            }
        }
    }
    random_device rd;
    mt19937 seed(rd()); // or seed(827)
    shuffle(neighbor_positions.begin(), neighbor_positions.end(), seed);
    int next_x = neighbor_positions[0][0], next_y = neighbor_positions[0][1], next_status = lattice->get_status(next_x, next_y), next_ID = lattice->get_ID(next_x, next_y);
    if(next_status == 0 | next_status == 5){
        lattice->switch_status(next_x, next_y, position_x, position_y, next_ID, ID);
        position_x = next_x; position_y = next_y;
    }
}

Citizen::Citizen(Lattice* lattice_ptr, int ID, int x, int y, int activeType): Agent(ID, x, y){
    this->activeType = activeType;
    active = (activeType == 1)? true : false;
    int status; // status -> -1:out of lattice; 0:unoccupied ; 1:LEO ; 2:citizen(quiescent) ; 3:citizen(active); 4 citizen(never acitve); 5 citizen(in jail)
    if(activeType == -1)
        status = 4;
    else if(activeType == 0)
        status = 2;
    else if(activeType == 1)
        status = 3;
    lattice_ptr->set_status_ID(position_x, position_y, status, ID);

    random_device rd;
    mt19937 seed(rd());
    uniform_real_distribution<> uni(0, 1.0);
    hardship = uni(seed);
    grievance = hardship * (1 - lattice_ptr->legitimacy);
    riskAversion = uni(seed);
    jail = -1;
}
void Citizen::set_perceivedNetRisk(Lattice* lattice, string functionForm){
    if(activeType == 0 & jail == -1){
        vector<vector<int> > a = lattice->get_status_in_vision(position_x, position_y, lattice->citizen_vision);
        int LEO_N = 0, activeCitizens_N = 0;
        for(int i = 0; i < a.size(); i++){
            if(a[i][2] == 1) 
                LEO_N++;
            else if(a[i][2] == 3)
                activeCitizens_N++;
        }
        float v = static_cast<float>(LEO_N) / 0.00000001;
        if(activeCitizens_N != 0)
            v = static_cast<float>(LEO_N) / static_cast<float>(activeCitizens_N);

        if(functionForm == "Step"){
            if(activeCitizens_N <= 4 * LEO_N)
                perceivedNetRisk = (1.0 - exp(-9.2104 * v)) * riskAversion;
            else
                perceivedNetRisk = 0;
        }
        else if(functionForm == "Sigmoidal"){
            float k = 62.6716, sum = 0.0, factorial_table[16] = {1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800, 479001600, 6227020800, 87178291200, 1307674368000};
            for(int i = 0; i <= 15; i++){
                sum += static_cast<float>(pow((k * v), i)) / factorial_table[i];
            }
            perceivedNetRisk = (1.0 - exp(-k * v) * sum) * riskAversion;
        }
        else
            cout << "GIVE A WRONG FUNCTION FORM!!!" << endl;

        active = (grievance - perceivedNetRisk > lattice->threshold) ? true : false;
        lattice->set_status_ID(position_x, position_y, active+2, ID);   
    } 
}
void Citizen::toJail(Lattice* lattice){
    lattice->set_status_ID(position_x, position_y, 5, ID);
    random_device rd;
    mt19937 seed(rd());
    uniform_int_distribution<> uni(0, lattice->jailMAX);
    jail = uni(seed);
}

LEO::LEO(Lattice* lattice_ptr, int ID, int x, int y): Agent(ID, x, y){
    lattice_ptr->set_status_ID(position_x, position_y, 1, ID);
}
// void LEO::arrest(Lattice* lattice, string functionForm){

// }