import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'compiler',
    pathMatch: 'full'
  },
  {
    path: 'compiler',
    loadChildren: () => import('./compilerhome/compilerhome.module').then(m => m.CompilerhomeComponentModule)
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
