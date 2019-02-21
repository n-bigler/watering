import React, { Component } from "react";
import ReactDOM from "react-dom";
import PropTypes from "prop-types";
import {Button, Grid} from "semantic-ui-react";

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
				<p>{this.props.desc}</p>
				<Button 
					content={this.props.name} 
					onClick={this.handleClick}
					key={this.props.name+"_buttonProcess"}
				/>
			</Grid.Column>
		);
	}
}

ProcessContainer.propTypes = {
	name: PropTypes.string.isRequired,
	desc: PropTypes.string
};

export default ProcessContainer;

