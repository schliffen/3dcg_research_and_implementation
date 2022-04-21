//
// Created by ek on 27.03.2022.
//

#ifndef INC_3DCG_RESEARCH_AND_IMPLEMENTATION_ENTITY_H
#define INC_3DCG_RESEARCH_AND_IMPLEMENTATION_ENTITY_H

#include <vector>
#include <iostream>
#include<GL/glut.h>
#include<math.h>
#include <iostream>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include "time.h"
#include <stack>
#include <map>
#include <glm/vec3.hpp>
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <SFML/Audio.hpp>
#include <SFML/Network.hpp>


class Entity {
private:

protected:
    sf::RectangleShape shape;
    float movementSpeed;

public:
    Entity();
    virtual ~Entity();
    //Functions
    virtual void move(const float& dt, const float x, const float y );
    virtual void update(const float & dt);
    virtual void render( sf::RenderTarget* target );
};


#endif //INC_3DCG_RESEARCH_AND_IMPLEMENTATION_ENTITY_H
