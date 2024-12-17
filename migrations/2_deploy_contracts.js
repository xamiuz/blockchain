const EmployeeContract = artifacts.require("EmployeeContract");

module.exports = function (deployer) {
  deployer.deploy(EmployeeContract);
};
