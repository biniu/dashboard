import React, {createContext} from "react";

import {Col, Row} from "react-bootstrap";

import Todos from "./Todos"
import Habits from "./Habits";
import Dailies from "./Dailies";

export const UserName = createContext("biniu");
export const UserID = createContext(1);

export default function UserDetails() {

    return (
        <Row>
            <Row>
                Habitica
            </Row>
            <Row>
            <Col>
                <UserName.Provider value={"biniu"}>
                    <UserID.Provider value={1}>
                        <Todos/>
                    </UserID.Provider>
                </UserName.Provider>
            </Col>
            <Col>
                <Row>
                    <UserName.Provider value={"biniu"}>
                        <UserID.Provider value={1}>
                            <Habits/>
                        </UserID.Provider>
                    </UserName.Provider>
                </Row>
                <Row>
                    <UserName.Provider value={"biniu"}>
                        <UserID.Provider value={1}>
                            <Dailies/>
                        </UserID.Provider>
                    </UserName.Provider>
                </Row>
            </Col>
            </Row>
        </Row>
    )
}