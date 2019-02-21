import React, { Component } from "react";
import ReactDOM from "react-dom";
import { Button } from 'semantic-ui-react';
import PropTypes from "prop-types";

class SwitchContainer extends Component {
	constructor(props) {
		super(props);
		this._isMounted = false;
		this.handleClick = this.handleClick.bind(this);
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
				  	if(result == "success"){
						var toSet = "on"
						this.state.state=="on" ? toSet = "off" : toSet = "on"
						this.setState({ state: toSet });
					}
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
