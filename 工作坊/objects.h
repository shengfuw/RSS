#include <string>
#include <math.h> 
#include <vector>
#include <fstream>
using namespace std;

inline float get_distant(int x1, int y1, int x2, int y2){
    return pow(pow((x1 - x2), 2) + pow((y1 - y2), 2), 0.5);
}

class Agent;
class Citizen;
class LEO;

class Lattice {
friend class Agent;
friend class Citizen;
friend class LEO;
private:
    int size, citizen_num, LEO_num, alwaysActive_start_index, neverActive_end_index, citizen_vision, LEO_vision, jailMAX, day;
    float citizen_density, alwaysActive, neverActive, legitimacy, threshold;
    string functionForm;
    vector<int> unoccupied_position_index;
    int** map;
    int** IDmap;
    int* IDs;
    Citizen** citizens;
    LEO** LEOs;
    
    int get_status(int x, int y) const;
    int get_ID(int x, int y) const;
    void set_status_ID(int x, int y, int status, int ID);
    void switch_status(int x1, int y1, int x2, int y2, int ID1, int ID2);
    vector<vector<int> > get_status_in_vision(int x, int y, int vision) const;
    void each_time_step();

public:
    Lattice(int size);
    ~Lattice();
    void place_agents(float citizen_density, int LEO_num, float alwaysActive, float neverActive, string functionForm, int citizen_vision, int LEO_vision, int jailMAX);
    void set_up_citizens();
    void get_info(ofstream& Myfile) const;
    void display(ofstream& Myfile) const;
};

class Agent {
protected:
    int ID, position_x, position_y;
public:   
    Agent(int ID, int x, int y);
    void move(Lattice* lattice_ptr);
};

class Citizen: public Agent {
friend class Lattice;
private:
    bool active;
    int activeType, jail;
    float hardship, grievance, riskAversion, perceivedNetRisk;

    Citizen(Lattice* lattice, int ID, int x, int y, int activeType);
    void set_perceivedNetRisk(Lattice* lattice_ptr, string functionForm);
    void toJail(Lattice* lattice_ptr);
};

class LEO: public Agent {
friend class Lattice;
private: 
    LEO(Lattice* lattice_ptr, int ID, int x, int y);
    void arrest(Lattice* lattice_ptr, string functionForm);
};