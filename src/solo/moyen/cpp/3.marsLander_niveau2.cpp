#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

struct Point
{
    Point()
    {
        m_x = 0;
        m_y = 0;
    }
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

struct LandingZone
{
    void setPointA(Point point)
    {
        m_pointA.m_x = point.m_x;
        m_pointA.m_y = point.m_y;
    }
    void setPointB(Point point)
    {
        m_pointB.m_x = point.m_x;
        m_pointB.m_y = point.m_y;
    }
    Point m_pointA;
    Point m_pointB;
};

void getLandingZone(std::vector<Point*> surfacePoints, LandingZone &landingZone)
{
    for (std::vector<Point*>::iterator i = surfacePoints.begin(); i != surfacePoints.end(); ++i)
    {
        if((*i)->m_y == (*(i+1))->m_y)
        {
            landingZone.setPointA(**i);
            landingZone.setPointB(**(i+1));
            break;
        }

    }
}

int main()
{
    int nbSurfacePoint; // the number of points used to draw the surface of Mars.
    int horizontalSpeed; // the horizontal speed (in m/s), can be negative.
    int verticalSpeed; // the vertical speed (in m/s), can be negative.
    int fuel; // the quantity of remaining fuel in liters.
    int landerRotation; // the rotation angle in degrees (-90 to 90).
    int power; // the thrust power (0 to 4).

    int verticalSpeedOrder = -40;
    int horizontalSpeedOrder = 20;
    int landerRotationOrder = 0;
    int errorVerticalSpeed;
    int errorHorizontalSpeed;
    std::vector<Point*> surfacePoints;
    LandingZone landingZone;
    Point lander;

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

    getLandingZone(surfacePoints, landingZone);

    cerr<<"----------- Landing zone --------------"<<endl;
    landingZone.m_pointA.display();
    landingZone.m_pointB.display();

    // game loop
    while (1)
    {
        cin >> lander.m_x >> lander.m_y >> horizontalSpeed >> verticalSpeed >> fuel >> landerRotation >> power; cin.ignore();

        if(landingZone.m_pointA.m_x < lander.m_x && lander.m_x < landingZone.m_pointB.m_x)
        {
            landerRotationOrder = 0;
            cerr<<"centre"<<endl;
        }
        else
        {
            if(landingZone.m_pointB.m_x < lander.m_x)
            {
                landerRotationOrder = 45;
                errorHorizontalSpeed = -horizontalSpeedOrder - horizontalSpeed;
            }
            else
            {
                landerRotationOrder = -45;
                errorHorizontalSpeed = horizontalSpeedOrder - horizontalSpeed;
            }
            cerr<<"errorHorizontalSpeed : "<<errorHorizontalSpeed<<endl;
            if(errorHorizontalSpeed < -18)
                landerRotationOrder = 45;
            if(errorHorizontalSpeed > 18)
                landerRotationOrder = -45;
        }
        errorVerticalSpeed = verticalSpeedOrder - verticalSpeed;
        power = (4-round(abs(errorVerticalSpeed / 10)));

        cout << landerRotationOrder <<" "<<power << endl; // R P. R is the desired rotation angle. P is the desired thrust power.
    }
}
