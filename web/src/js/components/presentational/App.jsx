import React from 'react';
import ReactDOM from "react-dom";
import SwitchGroupContainer from '../container/SwitchGroupContainer.jsx';
import ProcessesGroupContainer from '../container/ProcessesGroupContainer.jsx';
import LoggingContainer from '../container/LoggingContainer.jsx';
import WampContainer from '../container/WampContainer.jsx';
import { Container, Grid, Header } from 'semantic-ui-react';

const App = () => (
	<Container style={{ marginTop: '3em' }}>
		<Header as='h2' dividing>
			Switch
		</Header>
		<Grid centered>
			<WampContainer 
				url="ws://192.168.1.104:8080/ws"
				realm="realm1"
				channel="ch.watering.logging"
				>
					<SwitchGroupContainer />
			</WampContainer>
		</Grid>
		<Header as='h2' dividing>
			Logging
		</Header>
		<WampContainer 
			url="ws://192.168.1.104:8080/ws"
			realm="realm1"
			channel="ch.watering.logging"
			>
				<LoggingContainer />
		</WampContainer>
		<Header as='h2' dividing>
			Processes
		</Header>
		<Grid centered>
			<ProcessesGroupContainer />
		</Grid>
	</Container>
)

export default App;

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : false;
