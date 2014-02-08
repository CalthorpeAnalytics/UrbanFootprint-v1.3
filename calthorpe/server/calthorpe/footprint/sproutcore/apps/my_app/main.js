// ==========================================================================
// Project:   MyApp
// Copyright: @2013 My Company, Inc.
// ==========================================================================
/*globals MyApp */

// This is the function that will start your app running.  The default
// implementation will load any fixtures you have created then instantiate
// your controllers and awake the elements on your page.
//
// As you develop your application you will probably want to override this.
// See comments for some pointers on what to do next.
//
MyApp.main = function main() {

  // Step 1: Instantiate Your Views
  // The default code here will make the mainPane for your application visible
  // on screen.  If you app gets any level of complexity, you will probably
  // create multiple pages and panes.
  MyApp.getPath('mainPage.mainPane').append() ;

  // Step 2. Set the content property on your primary controller.
  // This will make your app come alive!
  //
  // ex.
  // var content = MyApp.store.find(MyApp.Group);
  // MyApp.groupsController.set('content', content);
 var content = [
    SC.Object.create({
      fname: 'John',
      lname: 'Doe',
      company: 'Google',
      title: 'Senior Manager'
    }),

    SC.Object.create({
      fname: 'Bob',
      lname: 'Smith',
      company: 'Microsoft',
      title: 'Sales'
    }),

    SC.Object.create({
      fname: 'Fred',
      lname: 'MacDoogle',
      company: 'Apple',
      title: 'Developer'
    })
  ];

  var controller = MyApp.testController;
  controller.set('content', content);

  var listView = MyApp.mainPage.mainPane.childViews[0].contentView;
  controller.set('listView', listView);

};


function main() { MyApp.main(); }
