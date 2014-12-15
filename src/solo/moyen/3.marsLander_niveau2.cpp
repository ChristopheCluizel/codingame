#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

struct Point
{
    Point(int x, int y)
    {
        m_x = x;
        m_y = y;
    }
    void display()
    {
        cerr<<"("<<m_x<<", "<<m_y<<")"<<endl;
    }

    int m_x;
    int m_y;
};

int main()
{
    int nbSurfacePoint; // the number of points used to draw the surface of Mars.
    std::vector<Point*> surfacePoints;

    cin >> nbSurfacePoint; cin.ignore();
    for (int i = 0; i < nbSurfacePoint; i++)
    {
        int surfacePoint_x; // X coordinate of a surface point. (0 to 6999)
        int surfacePoint_y; // Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
        cin >> surfacePoint_x >> surfacePoint_y; cin.ignore();
        surfacePoints.push_back(new Point(surfacePoint_x, surfacePoint_y));
    }

    // for (std::vector<Point*>::iterator i = surfacePoints.begin(); i != surfacePoints.end(); ++i)
    // {
    //     (*i)->display();
    // }

    // game loop
    while (1)
    {
        int lander_x;
        int lander_y;
        int horizontalSpeed; // the horizontal speed (in m/s), can be negative.
        int verticalSpeed; // the vertical speed (in m/s), can be negative.
        int fuel; // the quantity of remaining fuel in liters.
        int landerRotation; // the rotation angle in degrees (-90 to 90).
        int power; // the thrust power (0 to 4).
        cin >> lander_x >> lander_y >> horizontalSpeed >> verticalSpeed >> fuel >> landerRotation >> power; cin.ignore();


        cout << "-90 4" << endl; // R P. R is the desired rotation angle. P is the desired thrust power.
    }
}
