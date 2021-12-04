import React, {createContext} from "react";

import './CodeWars.css'
import {Col, Container, Row} from "react-bootstrap";

import UserDetails from "./UserDetails";
import StreaksView from "./StreaksView";
import {CircularProgressbar} from "react-circular-progressbar";
import LangInfo from "./LangInfo";

export const UserName = createContext("biniu");

export default function CodeWarsClient() {
    const percentage = 66;

    return (
        <Container fluid className={"codeWars"}>
            <Row className={"rowBorder"}>
                CodeWars
            </Row>
            <Row className={"rowBorder"}>
                <Col>
                    <Row className={"rowBorder"}>
                        <UserName.Provider value={"biniu"}>
                            <UserDetails/>
                        </UserName.Provider>
                    </Row>
                    <Row className={"rowBorder"}>
                        {/*<StreaksView/>*/}
                    </Row>
                </Col>

                <Col>
                    <Row className={"rowBorder"}>
                        {/*<LangInfo/>*/}
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

