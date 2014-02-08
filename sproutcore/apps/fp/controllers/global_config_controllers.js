
/***
 * globalConfigController binds holds the singleton global config as an array in its content to conform with the other
 * ConfigEntity controllers
 * @type {*}
 */
Footprint.globalConfigController = SC.ArrayController.create();

/***
 * References the globalConfig singleton in its content
 * @type {*|void}
 */
Footprint.globalConfigActiveController = Footprint.ActiveController.create({
    listController:Footprint.globalConfigController
});
