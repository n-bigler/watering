import React, { Component } from "react";
import PropTypes from "prop-types";

class Logging extends Component{

	constructor(props) {
		super(props);
	}

	render(){
		var msgList = [];
		for (let it = this.props.messages.length-1; it >= 0; it--){
			msgList.push(
				<li>{ this.props.messages[it] }</li>
			);
		}

		return (
			<ul>{msgList}</ul>
		);
	}
}

					

// const Logging = ({ messages }) => (
// 	<p>{ messages[0] }</p>
// );

Logging.propTypes = {
	messages: PropTypes.array.isRequired
};
export default Logging;
