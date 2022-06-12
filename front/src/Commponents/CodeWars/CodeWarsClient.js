import React, {createContext} from "react";

import './CodeWars.css'
import {Col, Container, Row} from "react-bootstrap";

import UserDetails from "./UserDetails";
import StreaksView from "./StreaksView";
// import {CircularProgressbar} from "react-circular-progressbar";
import LangInfo from "./LangInfo";

export const UserName = createContext("biniu");
export const UserID = createContext(1);

export default function CodeWarsClient() {
    // const percentage = 66;

    return (
        <Container fluid className={"codeWars"}>
            <Row>
                CodeWars
            </Row>
            <Row>
                <Col>
                    <Row>
                        <UserName.Provider value={"biniu"}>
                            <UserID.Provider value={1}>
                                <UserDetails/>
                            </UserID.Provider>
                        </UserName.Provider>
                    </Row>
                    <Row>
                        {/*<StreaksView/>*/}
                    </Row>
                </Col>

                <Col>
                    <Row>
                        <UserName.Provider value={"biniu"}>
                            <UserID.Provider value={1}>
                                <LangInfo/>
                            </UserID.Provider>
                        </UserName.Provider>
                    </Row>
                    {/*<Row className={"rowBorder"}>*/}
                    {/*    <CircularProgressbar value={percentage} text={`${percentage}%`}*/}
                    {/*    />*/}

                    {/*</Row>*/}
                </Col>
            </Row>
        </Container>


);
}

