#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <math.h>
#include "objects.h"
using namespace std;

int main() {
    cout << "Start !" << "\n";
    ofstream record_map("Maps.csv", ios::app), record_info("Info.csv", ios::in|ios::app);

    int size = 600;
    float citizen_density = 0.7, alwaysAcitve = 0.025, neverActive = 0.5;
    int LEO_num = size*size*citizen_density*1.51 / 1000;
    int vision = 14, jailMAx = 12;
    Lattice MyLattice(size);
    MyLattice.display(record_map); MyLattice.get_info(record_info);

    MyLattice.place_agents(citizen_density, LEO_num, alwaysAcitve, neverActive, "Step", vision, vision, jailMAx);
    MyLattice.display(record_map); MyLattice.get_info(record_info);
    
    MyLattice.set_up_citizens();
    MyLattice.display(record_map); MyLattice.get_info(record_info);

    cout << "Done !" << "\n";
}