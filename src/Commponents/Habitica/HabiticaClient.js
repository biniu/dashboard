import React from 'react';
import {Col, Container, Row} from "react-bootstrap";

import {CircularProgressbar} from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

class HabiticaClient extends React.Component {

    constructor(props) {
        super(props);
        this.URI = 'http://localhost:3001/codeWars'
        this.state = {data: []};
    }

    componentDidMount() {
        fetch(this.URI)
            .then(response => {
                return response.json();
            }).then(result => {
            this.setState({
                data: result
            });
        });
    }


    render() {
        const percentage = 66;

        return (
            <Container fluid>
                <Row className={"rowBorder"}>
                    <CircularProgressbar value={percentage} text={`${percentage}%`}
                    />

                </Row>
            </Container>
        )
    }
}

export default HabiticaClient;
