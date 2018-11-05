
Date.prototype.addDays = function(days) {
    this.setDate(this.getDate() + parseInt(days));
    return this;
};

Date.prototype.addMonths = function(months) {
    this.setMonth(this.getMonth() + parseInt(months));
    return this;
};

Date.prototype.addYears = function(years) {
    this.setFullYear(this.getFullYear() + parseInt(years));
    return this;
};
