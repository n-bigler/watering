import React from 'react';
import ReactDOM from "react-dom";
import SwitchGroupContainer from '../container/SwitchGroupContainer.jsx';
import ProcessesGroupContainer from '../container/ProcessesGroupContainer.jsx';
import LoggingContainer from '../container/LoggingContainer.jsx';
import { Container, Grid, Header } from 'semantic-ui-react';

const App = () => (
	<Container style={{ marginTop: '3em' }}>
		<Header as='h2' dividing>
			Switch
		</Header>
		<Grid centered>
				<SwitchGroupContainer />
		</Grid>
		<Header as='h2' dividing>
			Logging
		</Header>
		<LoggingContainer />
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
