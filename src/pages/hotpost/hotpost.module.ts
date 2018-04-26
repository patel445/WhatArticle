import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { HotPost } from './hotpost';

@NgModule({
  declarations: [
    HotPost
  ],
  imports: [
    IonicPageModule.forChild(HotPost),
  ],
})
export class HotPostModule {}