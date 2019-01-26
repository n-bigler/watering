import React from "react";
import PropTypes from "prop-types";
const Switch = ({ text, id, value, name, handleClick }) => (
	<div className="switch">
		<button
			type="button"
			className={value=="on" ? "btn-success" : "btn-danger"}
			name={name}
			value={value}
			onClick={handleClick}
		>
			{text}
		</button>
	</div>
);
Switch.propTypes = {
	text: PropTypes.string.isRequired,
	id: PropTypes.string.isRequired,
	value: PropTypes.string.isRequired,
  	name: PropTypes.string.isRequired,
	handleClick: PropTypes.func.isRequired
};
export default Switch;
