import React, { Component } from "react";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";
import {Button, Grid, Card, Input, Form, Icon} from "semantic-ui-react";

class TimerContainer extends Component {
	constructor(props) {
		super(props);
		this.delete = this.delete.bind(this);
	}

	delete(e){
		fetch(`http://192.168.1.104:5000/deletetimer?time=${this.props.time}`, {
		method: 'DELETE'
		})
		.then(response => response.text())
		.then(
			(result) => {
				console.log(result);
				this.props.getContent();
			}
		);
	}

	render() {

		console.log(this.props);
		return (
			<Grid.Column>
			<Card>
				<Card.Content>
					<Card.Header>{this.props.time}</Card.Header>
				</Card.Content>
				<Card.Content extra>
					Process to launch: {this.props.process}
				</Card.Content>
				<Card.Content>
						<Button negative icon labelPosition='right' onClick={this.delete}>
							<Icon name="trash alternate" />
							Delete timer
						</Button>
				</Card.Content>
			</Card>
			</Grid.Column>
		);
	}
}

TimerContainer.propTypes = {
	time: PropTypes.string.isRequired,
	process: PropTypes.string
};

export default TimerContainer;

