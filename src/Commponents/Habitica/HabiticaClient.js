import React from "react";

import Todos from "./Todos"
import {Col, Row} from "react-bootstrap";

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
                    Habits
                </Row>
                <Row>Dailies</Row>
            </Col>
            </Row>
        </Row>
    )
}