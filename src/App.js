
import './App.css';

import {Col, Container, Row} from "react-bootstrap";

import CodeWarsClient from "./Commponents/CodeWars/CodeWarsClient";
import HabiticaClient from "./Commponents/Habitica/HabiticaClient";

function App() {
  return (
    <div className="App">
      <header className="App-header">

          {/*<CodeWarsClient/>*/}

          <Container fluid className={"container100h"}>
              <Row className={"container50h"}>
                  <Col className={"colBorder"}>
                      <CodeWarsClient/>
                  </Col>
                  <Col className={"colBorder"}>
                      {/*<StreaksView/>*/}
                  </Col>
              </Row>
              <Row className={"container50h"}>
                  <Col className={"colBorder"}>
                      <HabiticaClient/>
                  </Col>
                  <Col className={"colBorder"}>2 of 3</Col>
                  <Col className={"colBorder"}>3 of 3</Col>
              </Row>
          </Container>
      </header>
    </div>
  );
}

export default App;
