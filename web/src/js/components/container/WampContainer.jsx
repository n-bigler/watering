import React, { Component } from "react";
import PropTypes from "prop-types";
import autobahn from "autobahn";



class WampContainer extends Component {
	constructor(props){
		super(props);
		this.state = {
			message: null
		};
		this.onNewMessage = this.onNewMessage.bind(this);
	}

	onNewMessage(args){
		let newMessage = args[0];
		this.setState((state, props) => {
			return {
				message: newMessage 
			}
		});
	}


	componentDidMount() {
		var connection = new autobahn.Connection({url: this.props.url, realm:this.props.realm});

		connection.onopen = ((session) => {
			session.subscribe(this.props.channel, this.onNewMessage);
		});
		connection.open();
	}

	render() {
		const children = React.Children.map(this.props.children, child => {
			return React.cloneElement(child, {
				message: this.state.message
			});
		});
		console.log(children);
		return (
			<div>
			{ children }
			</div>
		);
	}
}

WampContainer.propTypes = {
	url: PropTypes.string.isRequired,
	realm: PropTypes.string.isRequired,
	channel: PropTypes.string.isRequired
};
export default WampContainer;

