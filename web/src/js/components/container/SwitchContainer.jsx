import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Button } from 'semantic-ui-react';
import PropTypes from "prop-types";

class SwitchContainer extends Component {
	constructor(props) {
		super(props);
		this._isMounted = false;
		this.handleClick = this.handleClick.bind(this);
		console.log(this.props);
	}

	componentDidMount() {
		this._isMounted = true;
	}
	componentWillUnmount(){
		this._isMounted = false;
	}
	handleClick(event) {
		fetch(`http://192.168.1.104:5000/switch?name=${this.props.name}`,{
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
		let isOn = {'negative': true};
		if(this.props.isOn){
			isOn = {'positive': true};
		}
		return (
			<Button
				{...isOn}
				key={this.props.name+"_button"}
				content={this.props.name}
				onClick={this.handleClick}
			/>
		);
	}
}

SwitchContainer.propTypes = {
	name: PropTypes.string.isRequired,
	id: PropTypes.string.isRequired
};

export default SwitchContainer;
