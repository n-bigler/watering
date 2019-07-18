import React from 'react';
import ReactDOM from "react-dom";
import SwitchGroupContainer from '../container/SwitchGroupContainer.jsx';
import ProcessesGroupContainer from '../container/ProcessesGroupContainer.jsx';
import LoggingContainer from '../container/LoggingContainer.jsx';
import WampContainer from '../container/WampContainer.jsx';
import GroupContainer from '../container/GroupContainer.jsx';
import ProcessContainer from '../container/ProcessContainer.jsx';
import TimerContainer from '../container/TimerContainer.jsx';
import AddTimerContainer from '../container/AddTimerContainer.jsx';
import { Container, Grid, Header, Button, Icon, List} from 'semantic-ui-react';

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
			The Ugly Valve List
		</Header>
		<div>
			<List.List as='ol'>
				<List.Item as='li'>Lemongrass</List.Item>
				<List.Item as='li'>Pots sur la rambarde</List.Item>
				<List.Item as='li'>edamame au sol?</List.Item>
				<List.Item as='li'>Concombre?</List.Item>
				<List.Item as='li'>Tomates & Coriandre</List.Item>
				<List.Item as='li'>Basilic</List.Item>
				<List.Item as='li'>Tomates 2</List.Item>
			</List.List>
		</div>
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
			<GroupContainer url="http://192.168.1.104:5000/getallprocesses">
				<ProcessContainer name='' description=''/>
			</GroupContainer>
		</Grid>
		<Header as='h2' dividing>
			Timer
		</Header>
		<Grid centered>
			<GroupContainer url="http://192.168.1.104:5000/getalltimers">
				<TimerContainer time='' process=''/>
			</GroupContainer>
			<AddTimerContainer/>
		</Grid>

	</Container>
)

export default App;

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : false;
