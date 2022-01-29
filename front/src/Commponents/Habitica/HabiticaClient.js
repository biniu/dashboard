import React from "react";

import {Col, Row} from "react-bootstrap";

import Todos from "./Todos"
import Habits from "./Habits";
import Dailies from "./Dailies";

export default function UserDetails() {

    return (
        <Row>
            <Row>
                Habitica
            </Row>
            <Row>
            <Col>
                <Todos/>
            </Col>
            <Col>
                <Row>
                    {/*<Habits/>*/}
                </Row>
                <Row>
                    <Dailies/>
                </Row>
            </Col>
            </Row>
        </Row>
    )
}