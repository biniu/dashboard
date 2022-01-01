
import './GlobalCSS/theme.css';

import {Col, Container, Row} from "react-bootstrap";


import CodeWarsClient from "./Commponents/CodeWars/CodeWarsClient";
import HabiticaClient from "./Commponents/Habitica/HabiticaClient";


function App() {
  return (
    <div className="App">
      <header className="App-header">
          <Container fluid className={"container100h"}>
              <Row className={"container50h"}>
                  <Col className={"colBorder"}>
                        <CodeWarsClient/>
                  </Col>
                  <Col className={"colBorder"}>
                      ToDo
                  </Col>
              </Row>
              <Row className={"container50h"}>
                  <Col sm={8} className={"colBorder"}>
                      <HabiticaClient/>
                  </Col>
                  <Col className={"colBorder"}>
                      ToDo
                  </Col>
              </Row>
          </Container>
      </header>
    </div>
  );
}

export default App;
