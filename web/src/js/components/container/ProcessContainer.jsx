import React, { Component } from "react";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";
import {Button, Grid, Card, Input} from "semantic-ui-react";

class ProcessContainer extends Component {
	constructor(props) {
		super(props);
		this.handleClick = this.handleClick.bind(this);
	}


	componentDidMount() {
	}
	componentWillUnmount(){
	}


	handleClick(event) {
		console.log("clicked");
		fetch(`http://192.168.1.104:5000/launchprocess?name=${this.props.name}`,{
			method: 'POST'
		})
		.then(response => response.text())
		.then(
			(result) => {
				console.log(result);
			}
		);
	}

	render() {
		return (
			<Grid.Column>
			<Card>
				<Card.Content>
					<Card.Header>{this.props.name}</Card.Header>
					<Card.Description>{this.props.description}</Card.Description>
				</Card.Content>
				<Card.Content extra>
					<Button 
						content="Start"
						icon="play"
						labelPosition='left'
						onClick={this.handleClick}
						key={this.props.name+"_buttonProcess"}
					/>
				</Card.Content>
			</Card>
			</Grid.Column>
		);
	}
}

ProcessContainer.propTypes = {
	name: PropTypes.string.isRequired,
	description: PropTypes.string
};

export default ProcessContainer;

